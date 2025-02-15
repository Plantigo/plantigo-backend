from rest_framework import serializers

from .models import Device, Telemetry


class TelemetrySerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    device_mac = serializers.CharField(source='device.mac_address', read_only=True)

    class Meta:
        model = Telemetry
        fields = [
            'uuid',
            'device',
            'device_name',
            'device_mac',
            'temperature',
            'humidity',
            'pressure',
            'soil_moisture',
            'timestamp',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class DeviceSerializer(serializers.ModelSerializer):
    latest_telemetry = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(required=False)
    mac_address = serializers.CharField(required=False)

    class Meta:
        model = Device
        fields = [
            'uuid',
            'name',
            'mac_address',
            'user',
            'is_active',
            'latest_telemetry',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['is_active', 'created_at', 'updated_at']

    def validate(self, attrs):
        # For creation, ensure required fields are present
        if not self.instance:  # Creation
            if not attrs.get('name'):
                raise serializers.ValidationError({'name': 'This field is required for device creation.'})
            if not attrs.get('mac_address'):
                raise serializers.ValidationError({'mac_address': 'This field is required for device creation.'})
        return attrs

    def get_latest_telemetry(self, obj):
        latest_data = obj.get_latest_telemetry_data()
        return latest_data if latest_data else None


class DeviceDetailSerializer(DeviceSerializer):
    telemetry_history = serializers.SerializerMethodField()

    class Meta(DeviceSerializer.Meta):
        fields = DeviceSerializer.Meta.fields + ['telemetry_history']

    def get_telemetry_history(self, obj):
        hours = self.context.get('hours', 24)
        telemetry = obj.get_telemetry_history(hours=hours)
        return TelemetrySerializer(telemetry, many=True).data 