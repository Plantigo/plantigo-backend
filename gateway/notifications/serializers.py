from rest_framework import serializers
from .models import UserNotification


class UserNotificationSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    telemetry_data = serializers.SerializerMethodField()

    class Meta:
        model = UserNotification
        fields = [
            'uuid',
            'user',
            'device',
            'device_name',
            'telemetry',
            'telemetry_data',
            'message',
            'severity',
            'is_read',
            'read_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'user']

    def get_telemetry_data(self, obj):
        """Return relevant telemetry data that triggered the notification."""
        return {
            'temperature': obj.telemetry.temperature,
            'humidity': obj.telemetry.humidity,
            'pressure': obj.telemetry.pressure,
            'soil_moisture': obj.telemetry.soil_moisture,
            'timestamp': obj.telemetry.timestamp.isoformat(),
        } 