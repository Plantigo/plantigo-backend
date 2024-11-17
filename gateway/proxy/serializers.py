from rest_framework import serializers
from shared import devices_pb2
from plantigo_common.django.proto_serializer import ProtoSerializer


class DeviceProtoSerializer(ProtoSerializer):
    id = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    mac_address = serializers.CharField(max_length=100)

    class Meta:
        proto_class = devices_pb2.Device
