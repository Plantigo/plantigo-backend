import grpc
from devices import devices_pb2, devices_pb2_grpc

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMzcyOTE5LCJpYXQiOjE3MzE3NjgxMTksImp0aSI6IjI0ZmNkN2ZlM2JiYTQ2MDg4YzM0MGMwOGNlMDQ0MWQ1IiwidXNlcl9pZCI6IjVlODNlNjVjLTM4MDMtNDFiNS04ZTBhLTc1NjAwNTRhNDk2MyJ9.vTHoL2YMwttVv6jbvwo-jQOc-QmZXJeug4m6JJvixts"


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
