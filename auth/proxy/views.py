from rest_framework.decorators import api_view
from rest_framework.response import Response

from proxy.services import fetch_devices


@api_view()
def get_devices(request):

    try:
        devices = fetch_devices(request.user.id)
        device_list = [{'id': device.id, 'name': device.name} for device in devices]
        return Response({'devices': device_list})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
