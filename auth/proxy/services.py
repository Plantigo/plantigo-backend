import grpc
from grpc_interfaces.devices import devices_pb2
from grpc_interfaces.devices.devices_pb2_grpc import DeviceServiceStub


def fetch_devices(user_id: str) -> list[devices_pb2.Device]:
    """
    Fetches devices for a given user ID using gRPC.

    Args:
        user_id (str): The ID of the user whose devices are to be fetched.

    Returns:
        list: A list of devices associated with the user.
    """
    with grpc.insecure_channel('devices:50051') as channel:
        stub = DeviceServiceStub(channel)
        request = devices_pb2.DeviceRequest(user_id=user_id)
        response = stub.GetAllDevices(request)
    return response.devices
