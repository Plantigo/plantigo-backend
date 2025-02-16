import json
from typing import Optional, List, Tuple
from datetime import datetime
import logging
import pytz

import redis
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.db.models import Q

from devices.models import Device, Telemetry, DeviceSensorLimits
from notifications.models import UserNotification

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


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse timestamp string and convert to UTC timezone.
    Input timestamp is assumed to be in Europe/Warsaw timezone if no timezone info is provided.
    """
    # Parse the timestamp
    timestamp = datetime.fromisoformat(timestamp_str)
    
    # If timestamp is naive (no timezone info), assume it's in Europe/Warsaw
    if timestamp.tzinfo is None:
        local_tz = pytz.timezone('Europe/Warsaw')
        # Najpierw utwórz świadomy czasowo datetime w strefie Warsaw
        local_dt = local_tz.localize(timestamp, is_dst=None)
        # Następnie przekonwertuj do UTC
        utc_dt = local_dt.astimezone(pytz.UTC)
        logger.debug(f"Converted naive timestamp {timestamp_str} from Europe/Warsaw to UTC: {utc_dt}")
        return utc_dt
    
    # Jeśli timestamp już ma strefę czasową, po prostu przekonwertuj do UTC
    utc_dt = timestamp.astimezone(pytz.UTC)
    logger.debug(f"Converted aware timestamp {timestamp_str} to UTC: {utc_dt}")
    return utc_dt


def check_sensor_limits(telemetry: Telemetry) -> Tuple[List[str], str]:
    """
    Check if telemetry values are within defined limits.
    Returns tuple of (violation messages, severity level).
    """
    try:
        limits = telemetry.device.sensor_limits
    except DeviceSensorLimits.DoesNotExist:
        return [], 'info'
        
    violations = limits.check_limits(telemetry)
    
    # Determine severity based on number of violations
    if not violations:
        severity = 'info'
    elif len(violations) <= 2:
        severity = 'warning'
    else:
        severity = 'critical'
        
    return violations, severity


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
    4. Checks sensor limits and creates notifications
    5. Updates devices active status
    6. Schedules next execution
    
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
    batch_size = 100

    raw_data_batch: List[bytes] = []
    data_indices: List[int] = []
    
    queue_length = redis_client.llen(queue_key)
    batch_size = min(batch_size, queue_length)
    
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
    duplicates_count = 0
    notifications_count = 0
    telemetry_objects = []
    notification_objects = []
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
            
            # Parse and convert timestamp
            try:
                timestamp = parse_timestamp(telemetry_data['timestamp'])
                logger.debug(f"Parsed timestamp {telemetry_data['timestamp']} to UTC: {timestamp}")
            except (ValueError, pytz.exceptions.PytzError) as e:
                logger.error(f"Error parsing timestamp: {e}, Data: {telemetry_data['timestamp']}")
                errors_count += 1
                continue
            
            # Sprawdź czy istnieje już telemetria dla tego urządzenia i timestampu
            if Telemetry.objects.filter(
                device=device,
                timestamp=timestamp
            ).exists():
                logger.info(f"Duplicate telemetry found for device {mac_address} at {timestamp}")
                duplicates_count += 1
                successful_indices.append(index)  # Dodajemy do usunięcia z Redis
                continue
            
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
            
            # Check sensor limits and create notifications if needed
            violations, severity = check_sensor_limits(telemetry)
            if violations:
                notification = UserNotification(
                    user=device.user,
                    device=device,
                    telemetry=telemetry,
                    message="\n".join(violations),
                    severity=severity
                )
                notification_objects.append(notification)
                notifications_count += 1
                logger.info(f"Created {severity} notification for device {mac_address}: {violations}")
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Error processing telemetry data: {e}, Data: {raw_data}")
            errors_count += 1
            continue
    
    if not telemetry_objects:
        logger.warning(f"No valid telemetry data to process. Errors: {errors_count}, Duplicates: {duplicates_count}")
        # Usuń błędne i zduplikowane dane z kolejki
        if errors_count > 0 or duplicates_count > 0:
            logger.info("Removing invalid and duplicate data from queue")
            for _ in range(len(successful_indices)):
                redis_client.lpop(queue_key)
        self.apply_async(countdown=1)
        return f"No valid telemetry data to process. Errors: {errors_count}, Duplicates: {duplicates_count}"
    
    try:
        # Sort telemetry by timestamp to ensure chronological order
        telemetry_objects.sort(key=lambda x: x.timestamp)
        
        # Bulk create all telemetry records and notifications in transaction
        with transaction.atomic():
            logger.info(f"Starting bulk create of {len(telemetry_objects)} telemetry records")
            Telemetry.objects.bulk_create(telemetry_objects)
            
            if notification_objects:
                logger.info(f"Creating {len(notification_objects)} notifications")
                UserNotification.objects.bulk_create(notification_objects)
            
            # Update devices active status based on latest telemetry timestamp
            now = timezone.now()
            four_hours_ago = now - timezone.timedelta(hours=4)
            
            # Update active status for devices with recent data
            active_devices = Device.objects.filter(
                pk__in=devices_to_update,
                telemetry__timestamp__gte=four_hours_ago
            ).update(is_active=True)
            
            inactive_devices = Device.objects.filter(
                pk__in=devices_to_update,
                telemetry__timestamp__lt=four_hours_ago
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
                         f"({len(telemetry_objects)} saved, {errors_count} errors, "
                         f"{duplicates_count} duplicates, {notifications_count} notifications)")
        logger.info(result_message)
        return result_message
        
    except Exception as e:
        logger.error(f"Unexpected error during telemetry processing: {e}", exc_info=True)
        process_telemetry_queue.retry(exc=e)
