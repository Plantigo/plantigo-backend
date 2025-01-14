import grpc
from plantigo_common.django.proto_serializer import ProtoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from proxy.services import DevicesGRPCService, TelemetryGRPCService


@api_view(['GET'])
def get_data_for_period(request,mac_address):
    try:
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        dispatcher_service = TelemetryGRPCService(request)
        response = dispatcher_service.get_data_for_period(
            mac_address=mac_address, start_time=start_time, end_time=end_time
        )
        telemetry = ProtoSerializer(response.deviceData)
        return Response({'telemetry': telemetry.data}, status=200)
    except grpc.RpcError as e:
        return Response({'error': e.details()}, status=500)
    except Exception as e:
        return Response({'error': 'Server error'}, status=500)


@api_view(['GET'])
def get_average_data(request, mac_address):
    try:
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        dispatcher_service = TelemetryGRPCService(request)
        response = dispatcher_service.get_average_data(
            mac_address=mac_address, start_time=start_time, end_time=end_time
        )
        avg_temperature = ProtoSerializer(response.avg_temperature)
        avg_humidity = ProtoSerializer(response.avg_humidity)
        avg_pressure = ProtoSerializer(response.avg_pressure)
        avg_soil_moisture = ProtoSerializer(response.avg_soil_moisture)
        return Response(
            {'temperature': avg_temperature.data, "humidity": avg_humidity.data, "pressure": avg_pressure.data,
             "soil_moisture": avg_soil_moisture.data}, status=200)
    except grpc.RpcError as e:
        return Response({'error': e.details()}, status=500)
    except Exception as e:
        return Response({'error': 'Server error'}, status=500)


@api_view(['GET'])
def get_last_record(request, mac_address):
    try:
        dispatcher_service = TelemetryGRPCService(request)
        response = dispatcher_service.get_last_record(
            mac_address=mac_address)
        telemetry = ProtoSerializer(response.last_record)
        return Response({'telemetry': telemetry.data}, status=200)
    except grpc.RpcError as e:
        return Response({'error': e.details()}, status=500)
    except Exception as e:
        return Response({'error': 'Server error'}, status=500)


@api_view(['GET'])
def get_devices(request):
    """
    Retrieves a list of devices from the gRPC service.

    Args:
        request: The HTTP request object.

    Returns:
        Response: A DRF Response object containing the serialized list of devices or an error message.
    """
    try:
        devices_service = DevicesGRPCService(request)
        response = devices_service.get_all_devices()
        devices = ProtoSerializer(response.devices)
        return Response({'devices': devices.data}, status=200)
    except grpc.RpcError as e:
        return Response({'error': e.details()}, status=500)
    except Exception as e:
        return Response({'error': 'Server error'}, status=500)


@api_view(['POST'])
def create_device(request):
    """
    Creates a new device using the gRPC service.

    Args:
        request: The HTTP request object containing the device data. Required body args: `name` and `mac_address`.

    Returns:
        Response: A DRF Response object containing the serialized device or an error message.
    """
    try:
        name = request.data.get('name')
        mac_address = request.data.get('mac_address')

        if not name or not mac_address:
            return Response({'error': 'name and mac_address are required'}, status=400)

        devices_service = DevicesGRPCService(request)
        response = devices_service.create_device(
            name=name,
            mac_address=mac_address,
        )
        device = ProtoSerializer(response.device)
        return Response({'device': device.data}, status=200)
    except grpc.RpcError as e:
        return Response({'error': e.details()}, status=500)
    except Exception as e:
        return Response({'error': 'Server error'}, status=500)


@api_view(['PUT'])
def update_device(request, device_id):
    """
    Updates a device using the gRPC service.

    Args:
        request: The HTTP request object containing the device data. Available body args: `name`, `mac_address`.
        device_id: The ID of the device to update.

    Returns:
        Response: A DRF Response object containing the serialized device or an error message.
    """
    try:
        name = request.data.get('name')
        mac_address = request.data.get('mac_address')

        if not name and not mac_address:
            return Response({'error': 'Either name or mac_address is required'}, status=400)

        devices_service = DevicesGRPCService(request)
        response = devices_service.update_device(
            id=device_id,
            name=name,
            mac_address=mac_address,
        )
        device = ProtoSerializer(response.device)
        return Response({'device': device.data}, status=200)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            return Response({'error': 'Device not found'}, status=404)
        return Response({'error': e.details()}, status=500)
    except Exception as e:
        return Response({'error': 'Server error'}, status=500)


@api_view(['DELETE'])
def delete_device(request, device_id):
    """
    Deletes a device using the gRPC service.

    Args:
        request: The HTTP request object.
        device_id: The ID of the device to delete.

    Returns:
        Response: A DRF Response object containing the success message or an error message.
    """
    try:
        devices_service = DevicesGRPCService(request)
        devices_service.delete_device(id=device_id)
        return Response({'message': 'Device deleted'}, status=200)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            return Response({'error': 'Device not found'}, status=404)
        return Response({'error': e.details()}, status=500)
    except Exception as e:
        return Response({'error': 'Server error'}, status=500)
