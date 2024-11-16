import grpc
from devices import devices_pb2, devices_pb2_grpc

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxNzYzMDE1LCJpYXQiOjE3MzE3NjEyMTUsImp0aSI6Ijg4MDBmODJjNmU0ZjQ3Y2FhNGFlZjZhOTgxZWVlODhhIiwidXNlcl9pZCI6IjVlODNlNjVjLTM4MDMtNDFiNS04ZTBhLTc1NjAwNTRhNDk2MyJ9.sdaewi9z74vXinCPyCdQcDC0rtZk-ZiJBrW3Y22DjoE"


def test_get_all_devices():
    metadata = [("authorization", f"Bearer {token}")]

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = devices_pb2_grpc.DeviceServiceStub(channel)

        request = devices_pb2.GetDevicesRequest()

        try:
            response = stub.GetAllDevices(request, metadata=metadata)
            print("Devices received from server:")
            for device in response.devices:
                print(f"ID: {device.id}, Name: {device.name}, MAC Address: {device.mac_address}")
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()}, {e.details()}")


if __name__ == "__main__":
    test_get_all_devices()
