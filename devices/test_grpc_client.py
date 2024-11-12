import grpc
from devices import devices_pb2, devices_pb2_grpc


def test_get_all_devices():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = devices_pb2_grpc.DeviceServiceStub(channel)

        request = devices_pb2.GetDevicesRequest(user_id="5e83e65c-3803-41b5-8e0a-7560054a4963")  # Użyj rzeczywistego user_id

        try:
            response = stub.GetAllDevices(request)
            print("Devices received from server:")
            for device in response.devices:
                print(f"ID: {device.id}, Name: {device.name}, MAC Address: {device.mac_address}")
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()}, {e.details()}")


if __name__ == "__main__":
    test_get_all_devices()
