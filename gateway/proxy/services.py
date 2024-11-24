from django.conf import settings
from plantigo_common.python.grpc.rpc_caller import create_grpc_services_factory

from shared.devices_pb2_grpc import DeviceServiceStub
from shared import devices_pb2

grpc_config = {
    "devices": {
        "stub": DeviceServiceStub,
        "address": settings.DEVICES_SERVICE_URL,
        "request_classes": {
            "GetAllDevices": devices_pb2.GetDevicesRequest,
            "CreateDevice": devices_pb2.CreateDeviceRequest,
            "UpdateDevice": devices_pb2.UpdateDeviceRequest,
            "DeleteDevice": devices_pb2.DeleteDeviceRequest,
        },
    },
}

factory = create_grpc_services_factory(config_dict=grpc_config)
DevicesGRPCService = factory.create_service_class("devices")
