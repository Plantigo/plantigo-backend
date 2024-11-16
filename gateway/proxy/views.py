from rest_framework.decorators import api_view
from rest_framework.response import Response

from proxy.grpc_caller import GRPCServiceFactory
from google.protobuf.json_format import MessageToDict

DevicesGRPCService = GRPCServiceFactory.create_service_class("devices")


@api_view()
def get_devices(request):
    try:
        devices_service = DevicesGRPCService(request)
        response = devices_service.get_all_devices()
        device_list = [MessageToDict(data) for data in response.devices]
        return Response({'devices': device_list})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
