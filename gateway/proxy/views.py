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
        serializer = ProtoSerializer(response.devices, many=True)
        return Response({'devices': serializer.data}, status=200)
    except Exception as e:
        return Response({'error': 'Server error'}, status=500)


@api_view(['POST'])
def create_device(request):
    """
    Creates a new device using the gRPC service.

    Args:
        request: The HTTP request object.

    Returns:
        Response: A DRF Response object containing the serialized device or an error message.
    """
    try:
        devices_service = DevicesGRPCService(request)
        response = devices_service.create_device(request.data)
        serializer = DeviceProtoSerializer(response.device)
        return Response({'device': serializer.data}, status=200)
    except Exception as e:
        return Response({'error': 'Server error'}, status=500)
