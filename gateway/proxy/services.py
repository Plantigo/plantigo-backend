from django.conf import settings
from plantigo_common.python.grpc.rpc_caller import create_grpc_services_factory

from shared import devices_pb2, dispatcher_pb2
from shared.devices_pb2_grpc import DeviceServiceStub
from shared.dispatcher_pb2_grpc import DispatcherStub

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
    "telemetry": {
        "stub": DispatcherStub,
        "address": settings.TELEMETRY_SERVICE_URL,
        "request_classes": {
            "GetDataForPeriod": dispatcher_pb2.TimeRangeRequest,
            "GetAverageData": dispatcher_pb2.AverageRequest,
            "GetLastRecord": dispatcher_pb2.LastRecordRequest
        }
    }

}

factory = create_grpc_services_factory(config_dict=grpc_config)
TelemetryGRPCService = factory.create_service_class("telemetry")
DevicesGRPCService = factory.create_service_class("devices")
