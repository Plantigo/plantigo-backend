# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import devices.devices_pb2 as devices__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in devices_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class DeviceServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAllDevices = channel.unary_unary(
                '/devices.DeviceService/GetAllDevices',
                request_serializer=devices__pb2.GetDevicesRequest.SerializeToString,
                response_deserializer=devices__pb2.GetDevicesResponse.FromString,
                _registered_method=True)
        self.CreateDevice = channel.unary_unary(
                '/devices.DeviceService/CreateDevice',
                request_serializer=devices__pb2.CreateDeviceRequest.SerializeToString,
                response_deserializer=devices__pb2.CreateDeviceResponse.FromString,
                _registered_method=True)
        self.UpdateDevice = channel.unary_unary(
                '/devices.DeviceService/UpdateDevice',
                request_serializer=devices__pb2.UpdateDeviceRequest.SerializeToString,
                response_deserializer=devices__pb2.UpdateDeviceResponse.FromString,
                _registered_method=True)
        self.DeleteDevice = channel.unary_unary(
                '/devices.DeviceService/DeleteDevice',
                request_serializer=devices__pb2.DeleteDeviceRequest.SerializeToString,
                response_deserializer=devices__pb2.DeleteDeviceResponse.FromString,
                _registered_method=True)


class DeviceServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAllDevices(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateDevice(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDevice(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDevice(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DeviceServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAllDevices': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllDevices,
                    request_deserializer=devices__pb2.GetDevicesRequest.FromString,
                    response_serializer=devices__pb2.GetDevicesResponse.SerializeToString,
            ),
            'CreateDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateDevice,
                    request_deserializer=devices__pb2.CreateDeviceRequest.FromString,
                    response_serializer=devices__pb2.CreateDeviceResponse.SerializeToString,
            ),
            'UpdateDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateDevice,
                    request_deserializer=devices__pb2.UpdateDeviceRequest.FromString,
                    response_serializer=devices__pb2.UpdateDeviceResponse.SerializeToString,
            ),
            'DeleteDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteDevice,
                    request_deserializer=devices__pb2.DeleteDeviceRequest.FromString,
                    response_serializer=devices__pb2.DeleteDeviceResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'devices.DeviceService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('devices.DeviceService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class DeviceService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAllDevices(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/devices.DeviceService/GetAllDevices',
            devices__pb2.GetDevicesRequest.SerializeToString,
            devices__pb2.GetDevicesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CreateDevice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/devices.DeviceService/CreateDevice',
            devices__pb2.CreateDeviceRequest.SerializeToString,
            devices__pb2.CreateDeviceResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateDevice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/devices.DeviceService/UpdateDevice',
            devices__pb2.UpdateDeviceRequest.SerializeToString,
            devices__pb2.UpdateDeviceResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteDevice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/devices.DeviceService/DeleteDevice',
            devices__pb2.DeleteDeviceRequest.SerializeToString,
            devices__pb2.DeleteDeviceResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
