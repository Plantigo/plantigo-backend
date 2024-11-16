# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from dispatcher import dispatcher_pb2 as dispatcher_dot_dispatcher__pb2

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
        + f' but the generated code in dispatcher/dispatcher_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class DispatcherStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendDeviceData = channel.unary_unary(
                '/dispatcher.Dispatcher/SendDeviceData',
                request_serializer=dispatcher_dot_dispatcher__pb2.DeviceData.SerializeToString,
                response_deserializer=dispatcher_dot_dispatcher__pb2.Response.FromString,
                _registered_method=True)
        self.GetDataForPeriod = channel.unary_unary(
                '/dispatcher.Dispatcher/GetDataForPeriod',
                request_serializer=dispatcher_dot_dispatcher__pb2.TimeRangeRequest.SerializeToString,
                response_deserializer=dispatcher_dot_dispatcher__pb2.Response.FromString,
                _registered_method=True)
        self.GetAverageData = channel.unary_unary(
                '/dispatcher.Dispatcher/GetAverageData',
                request_serializer=dispatcher_dot_dispatcher__pb2.AverageRequest.SerializeToString,
                response_deserializer=dispatcher_dot_dispatcher__pb2.AverageResponse.FromString,
                _registered_method=True)
        self.GetLastRecord = channel.unary_unary(
                '/dispatcher.Dispatcher/GetLastRecord',
                request_serializer=dispatcher_dot_dispatcher__pb2.LastRecordRequest.SerializeToString,
                response_deserializer=dispatcher_dot_dispatcher__pb2.LastRecordResponse.FromString,
                _registered_method=True)


class DispatcherServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendDeviceData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDataForPeriod(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAverageData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLastRecord(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DispatcherServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendDeviceData': grpc.unary_unary_rpc_method_handler(
                    servicer.SendDeviceData,
                    request_deserializer=dispatcher_dot_dispatcher__pb2.DeviceData.FromString,
                    response_serializer=dispatcher_dot_dispatcher__pb2.Response.SerializeToString,
            ),
            'GetDataForPeriod': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDataForPeriod,
                    request_deserializer=dispatcher_dot_dispatcher__pb2.TimeRangeRequest.FromString,
                    response_serializer=dispatcher_dot_dispatcher__pb2.Response.SerializeToString,
            ),
            'GetAverageData': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAverageData,
                    request_deserializer=dispatcher_dot_dispatcher__pb2.AverageRequest.FromString,
                    response_serializer=dispatcher_dot_dispatcher__pb2.AverageResponse.SerializeToString,
            ),
            'GetLastRecord': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLastRecord,
                    request_deserializer=dispatcher_dot_dispatcher__pb2.LastRecordRequest.FromString,
                    response_serializer=dispatcher_dot_dispatcher__pb2.LastRecordResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dispatcher.Dispatcher', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('dispatcher.Dispatcher', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Dispatcher(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendDeviceData(request,
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
            '/dispatcher.Dispatcher/SendDeviceData',
            dispatcher_dot_dispatcher__pb2.DeviceData.SerializeToString,
            dispatcher_dot_dispatcher__pb2.Response.FromString,
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
    def GetDataForPeriod(request,
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
            '/dispatcher.Dispatcher/GetDataForPeriod',
            dispatcher_dot_dispatcher__pb2.TimeRangeRequest.SerializeToString,
            dispatcher_dot_dispatcher__pb2.Response.FromString,
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
    def GetAverageData(request,
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
            '/dispatcher.Dispatcher/GetAverageData',
            dispatcher_dot_dispatcher__pb2.AverageRequest.SerializeToString,
            dispatcher_dot_dispatcher__pb2.AverageResponse.FromString,
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
    def GetLastRecord(request,
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
            '/dispatcher.Dispatcher/GetLastRecord',
            dispatcher_dot_dispatcher__pb2.LastRecordRequest.SerializeToString,
            dispatcher_dot_dispatcher__pb2.LastRecordResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
