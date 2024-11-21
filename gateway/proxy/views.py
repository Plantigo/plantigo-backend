from rest_framework.decorators import api_view
from rest_framework.response import Response
from proxy.services import DevicesGRPCService
from plantigo_common.django.proto_serializer import ProtoSerializer


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
    except Exception as e:
        return Response({'error': 'Server error'}, status=500)
