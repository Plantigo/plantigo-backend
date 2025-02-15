from __future__ import annotations

import json
from datetime import timedelta
from typing import Dict, Optional, Any

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet, Subquery
from django.db.models import ExpressionWrapper, BooleanField, Q, F, Value
from django.utils import timezone

from core.models import BaseModel

User = get_user_model()


class Telemetry(BaseModel):
    """
    Model representing telemetry data received from IoT devices.
    
    Stores environmental measurements like temperature, humidity, pressure,
    and soil moisture along with the timestamp of measurement.
    """
    device = models.ForeignKey(
        'Device',
        on_delete=models.CASCADE,
        help_text="Device that sent this telemetry data"
    )
    temperature = models.FloatField(
        help_text="Temperature in Celsius"
    )
    humidity = models.FloatField(
        help_text="Relative humidity in percentage"
    )
    pressure = models.FloatField(
        help_text="Atmospheric pressure in hPa"
    )
    soil_moisture = models.IntegerField(
        help_text="Soil moisture level (raw sensor value)"
    )
    timestamp = models.DateTimeField(
        help_text="Time when the measurement was taken"
    )

    class Meta:
        verbose_name_plural = "Telemetries"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['device', 'timestamp']),
        ]
        get_latest_by = 'timestamp'

    def __str__(self) -> str:
        return f"Telemetry for {self.device.name} at {self.timestamp.isoformat()}"

    def to_dict(self) -> Dict[str, Any]:
        """Returns telemetry data as a dictionary."""
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'soil_moisture': self.soil_moisture,
            'timestamp': self.timestamp.isoformat(),
            'device_name': self.device.name,
            'device_mac': self.device.mac_address,
        }

    def save(self, *args, **kwargs):
        """Override save to update device active status."""
        super().save(*args, **kwargs)
        self.device.update_active_status()


class Device(BaseModel):
    """
    Model representing an IoT device with telemetry capabilities.
    
    The device is considered active if it has sent telemetry data within the last 5 minutes.
    """
    name = models.CharField(
        max_length=255,
        help_text="Name of the device"
    )
    mac_address = models.CharField(
        max_length=17,
        unique=True,
        help_text="MAC address of the device (format: XX:XX:XX:XX:XX:XX)"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='devices',
        help_text="User who owns this device"
    )
    is_active = models.BooleanField(
        default=False,
        help_text="Indicates if device is active (has sent data in last 5 minutes)"
    )

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['mac_address']),
            models.Index(fields=['user', 'is_active'])
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.mac_address})"

    def update_active_status(self) -> bool:
        """Updates the is_active status based on recent telemetry data."""
        has_recent_data = self.telemetry_set.filter(
            timestamp__gte=timezone.now() - timedelta(minutes=5)
        ).exists()
        if self.is_active != has_recent_data:
            self.is_active = has_recent_data
            self.save(update_fields=['is_active'])
        return self.is_active

    def get_telemetry(self) -> QuerySet[Telemetry]:
        """Returns all telemetry data for this device, ordered by timestamp descending."""
        return self.telemetry_set.order_by('-timestamp')

    def get_latest_telemetry(self) -> Optional[Telemetry]:
        """Returns the most recent telemetry data for this device."""
        return self.telemetry_set.order_by('-timestamp').first()

    def get_latest_telemetry_data(self) -> Optional[Dict[str, Any]]:
        """Returns the most recent telemetry data as a dictionary."""
        telemetry = self.get_latest_telemetry()
        if not telemetry:
            return None
            
        return {
            'temperature': telemetry.temperature,
            'humidity': telemetry.humidity,
            'pressure': telemetry.pressure,
            'soil_moisture': telemetry.soil_moisture,
            'timestamp': telemetry.timestamp.isoformat(),
        }

    def get_latest_telemetry_data_as_json(self) -> Optional[str]:
        """Returns the most recent telemetry data as a JSON string."""
        data = self.get_latest_telemetry_data()
        return json.dumps(data) if data else None

    def get_telemetry_history(self, hours: int = 24) -> QuerySet[Telemetry]:
        """Returns telemetry history for specified number of hours."""
        time_threshold = timezone.now() - timedelta(hours=hours)
        return self.telemetry_set.filter(
            timestamp__gte=time_threshold
        ).order_by('-timestamp')

