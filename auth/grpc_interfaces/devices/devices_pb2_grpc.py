# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import grpc_interfaces.devices.devices_pb2 as devices__pb2

GRPC_GENERATED_VERSION = '1.67.1'
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
    """Definicja serwisu
    """

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


class DeviceServiceServicer(object):
    """Definicja serwisu
    """

    def GetAllDevices(self, request, context):
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
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'devices.DeviceService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('devices.DeviceService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class DeviceService(object):
    """Definicja serwisu
    """

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
