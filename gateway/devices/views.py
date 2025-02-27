from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from devices.models import Device, Telemetry
from devices.serializers import DeviceSerializer, TelemetrySerializer, DeviceDetailSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing IoT devices.

    list:
        Get list of all user's devices with their latest telemetry data
    retrieve:
        Get detailed device information including telemetry history
    create:
        Register new device
    update:
        Update device information (PUT)
    partial_update:
        Update specific device fields (PATCH)
    delete:
        Remove device (hard delete)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DeviceDetailSerializer
        return DeviceSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Perform hard delete of the device."""
        instance = self.get_object()
        instance.hard_delete()
        return Response(status=204)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get device telemetry history with optional time range."""
        device = self.get_object()
        hours = int(request.query_params.get('hours', 24))

        serializer = DeviceDetailSerializer(
            device,
            context={'hours': hours}
        )
        return Response(serializer.data)


class TelemetryViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    ViewSet for managing telemetry data.

    list:
        Get list of telemetry data (filtered by device if specified)
    retrieve:
        Get specific telemetry record
    create:
        Add new telemetry data
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TelemetrySerializer

    def get_queryset(self):
        queryset = Telemetry.objects.filter(device__user=self.request.user)

        # Filter by device if specified
        device_id = self.request.query_params.get('device', None)
        if device_id:
            queryset = queryset.filter(device_id=device_id)

        # Filter by time range if specified
        hours = self.request.query_params.get('hours', None)
        if hours:
            time_threshold = timezone.now() - timedelta(hours=int(hours))
            queryset = queryset.filter(timestamp__gte=time_threshold)

        return queryset
