from rest_framework.decorators import api_view
from rest_framework.response import Response

from proxy.services import fetch_devices
from google.protobuf.json_format import MessageToDict


@api_view()
def get_devices(request):
    """
    Retrieve a list of devices.

    This view fetches devices using the `fetch_devices` service and returns
    a JSON response containing a list of devices with their id, name, and
    mac_address. In case of an error, it returns a JSON response with the
    error message and a 500 status code.

    Args:
        request: The HTTP request object.

    Returns:
        Response: A JSON response with the list of devices or an error message.
    """
    try:
        devices = fetch_devices(request)
        device_list = [MessageToDict(data) for data in devices]
        return Response({'devices': device_list})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
