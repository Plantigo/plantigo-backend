import grpc
from rest_framework.request import Request

from shared import devices_pb2
from shared.devices_pb2_grpc import DeviceServiceStub


def fetch_devices(request: Request) -> list[devices_pb2.Device]:
    """
    Fetches a list of devices from the gRPC DeviceService.

    Args:
        request (Request): The HTTP request object containing authentication information.

    Returns:
        list[devices_pb2.Device]: A list of devices retrieved from the gRPC service.
    """
    metadata = [("authorization", f"Bearer {request.auth.token.decode('utf-8')}")]

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = DeviceServiceStub(channel)
        request = devices_pb2.GetDevicesRequest()
        response = stub.GetAllDevices(request, metadata=metadata)
    return response.devices
