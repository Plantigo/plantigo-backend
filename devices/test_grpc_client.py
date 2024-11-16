import grpc
from devices import devices_pb2, devices_pb2_grpc

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxNjE1OTMwLCJpYXQiOjE3MzE2MTQxMzAsImp0aSI6ImQ1MTFhMzk2YmRkZTQ2MmU5NTBhMzIyYTJiZTJlMGYyIiwidXNlcl9pZCI6IjVlODNlNjVjLTM4MDMtNDFiNS04ZTBhLTc1NjAwNTRhNDk2MyJ9.PiQ5xB-n28HmtbqGWKnL66eQ4O4Q_Oh6fgI7j6i2i2s'


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
