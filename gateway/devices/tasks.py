import json
from typing import Optional, List
from datetime import datetime
import logging

import redis
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.db import transaction

from devices.models import Device, Telemetry

logger = logging.getLogger(__name__)


def format_mac_address(mac: str) -> str:
    """
    Format MAC address from raw format (e.g. '10061c41d104') 
    to standard format (e.g. '10:06:1C:41:D1:04')
    """
    # Remove any existing colons and convert to uppercase
    mac = mac.replace(':', '').upper()
    # Insert colons every 2 characters
    return ':'.join(mac[i:i+2] for i in range(0, len(mac), 2))


@shared_task(
    name="process_telemetry_queue",
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
    bind=True
)
def process_telemetry_queue(self) -> Optional[str]:
    """
    Process telemetry data from Redis queue.
    
    The task:
    1. Gets batch of data from Redis queue
    2. Validates devices existence by MAC address
    3. Creates telemetry records in bulk
    4. Updates devices active status
    5. Schedules next execution
    
    Returns:
        Optional[str]: Message about processing result
    """
    logger.info("Starting telemetry queue processing")
    
    # Connect to Redis using settings
    try:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=False)
        logger.debug("Successfully connected to Redis")
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise
    
    queue_key = "telemetry_queue"
    batch_size = 100  # Process 100 records at a time
    
    # Get batch of data from Redis queue (non-blocking)
    raw_data_batch: List[bytes] = []
    data_indices: List[int] = []
    
    # Najpierw sprawdź długość kolejki
    queue_length = redis_client.llen(queue_key)
    batch_size = min(batch_size, queue_length)
    
    # Pobierz dane bez usuwania
    for index in range(batch_size):
        raw_data = redis_client.lindex(queue_key, index)
        if raw_data:
            raw_data_batch.append(raw_data)
            data_indices.append(index)
    
    logger.info(f"Retrieved {len(raw_data_batch)} records from Redis queue (total queue size: {queue_length})")
    
    if not raw_data_batch:
        logger.debug("No data in queue, scheduling next execution")
        self.apply_async(countdown=1)
        return None
        
    processed_count = 0
    errors_count = 0
    telemetry_objects = []
    devices_to_update = set()
    successful_indices = []  # Indeksy danych, które zostały pomyślnie przetworzone
    
    # Process all records in batch
    for index, raw_data in zip(data_indices, raw_data_batch):
        try:
            # Parse telemetry data
            telemetry_data = json.loads(raw_data)
            
            # Format MAC address to standard format
            mac_address = format_mac_address(telemetry_data['mac_address'])
            logger.debug(f"Processing telemetry for device: {mac_address}")
            
            # Find device by MAC address
            try:
                device = Device.objects.get(mac_address=mac_address)
            except Device.DoesNotExist:
                logger.warning(f"Device not found for MAC address: {mac_address}")
                errors_count += 1
                continue
            
            # Parse timestamp from data
            timestamp = datetime.fromisoformat(telemetry_data['timestamp'])
            
            # Create telemetry object with device
            telemetry = Telemetry(
                device=device,
                temperature=telemetry_data['temperature'],
                humidity=telemetry_data['humidity'],
                pressure=telemetry_data['pressure'],
                soil_moisture=telemetry_data['soil_moisture'],
                timestamp=timestamp
            )
            telemetry_objects.append(telemetry)
            devices_to_update.add(device.pk)
            processed_count += 1
            successful_indices.append(index)
            logger.debug(f"Successfully processed telemetry for device: {mac_address}")
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Error processing telemetry data: {e}, Data: {raw_data}")
            errors_count += 1
            continue
    
    if not telemetry_objects:
        logger.warning(f"No valid telemetry data to process. Errors: {errors_count}")
        # Usuń błędne dane z kolejki
        if errors_count > 0:
            logger.info("Removing invalid data from queue")
            for _ in range(len(data_indices)):
                redis_client.lpop(queue_key)
        self.apply_async(countdown=1)
        return f"No valid telemetry data to process. Errors: {errors_count}"
    
    try:
        # Sort telemetry by timestamp to ensure chronological order
        telemetry_objects.sort(key=lambda x: x.timestamp)
        
        # Bulk create all telemetry records in transaction
        with transaction.atomic():
            logger.info(f"Starting bulk create of {len(telemetry_objects)} telemetry records")
            Telemetry.objects.bulk_create(telemetry_objects)
            
            # Update devices active status based on latest telemetry timestamp
            now = timezone.now()
            five_minutes_ago = now - timezone.timedelta(minutes=5)
            
            # Update active status for devices with recent data
            active_devices = Device.objects.filter(
                pk__in=devices_to_update,
                telemetry__timestamp__gte=five_minutes_ago
            ).update(is_active=True)
            
            inactive_devices = Device.objects.filter(
                pk__in=devices_to_update,
                telemetry__timestamp__lt=five_minutes_ago
            ).update(is_active=False)
            
            logger.info(f"Updated device statuses: {active_devices} active, {inactive_devices} inactive")
            
            # Po pomyślnym zapisie do bazy, usuń przetworzone dane z kolejki
            logger.info(f"Removing {len(successful_indices)} processed records from Redis queue")
            for _ in range(len(successful_indices)):
                redis_client.lpop(queue_key)
        
        # Schedule next execution immediately
        logger.info("Scheduling next execution")
        self.apply_async()
        
        result_message = (f"Processed {processed_count} telemetry records "
                         f"({len(telemetry_objects)} saved, {errors_count} errors)")
        logger.info(result_message)
        return result_message
        
    except Exception as e:
        logger.error(f"Unexpected error during telemetry processing: {e}", exc_info=True)
        process_telemetry_queue.retry(exc=e)
