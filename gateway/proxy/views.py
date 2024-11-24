from proxy.services import DevicesGRPCService
from rest_framework.decorators import api_view
from rest_framework.response import Response
import grpc
from django.urls import path
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


class GRPCViewSet:
    """
    Bazowa klasa dla ViewSetów obsługujących serwisy gRPC.
    Automatycznie generuje endpointy REST na podstawie zdefiniowanych akcji.
    """
    grpc_service_class = None
    url_prefix = ''

    # Domyślne mapowanie akcji na metody HTTP
    default_actions = {
        'list': {'method': 'GET', 'url': '', 'grpc_method': 'get_all_{resource}s'},
        'retrieve': {'method': 'GET', 'url': '{id}', 'grpc_method': 'get_{resource}'},
        'create': {'method': 'POST', 'url': '', 'grpc_method': 'create_{resource}'},
        'update': {'method': 'PUT', 'url': '{id}', 'grpc_method': 'update_{resource}'},
        'delete': {'method': 'DELETE', 'url': '{id}', 'grpc_method': 'delete_{resource}'}
    }

    # Można nadpisać w klasach pochodnych
    actions = {}

    @classmethod
    def get_grpc_method_name(cls, action, resource=None):
        """Zwraca nazwę metody gRPC dla danej akcji"""
        resource = resource or cls.get_resource_name()
        action_config = cls.get_actions().get(action, {})
        return action_config.get('grpc_method', '').format(resource=resource)

    @classmethod
    def get_resource_name(cls):
        """Zwraca nazwę zasobu na podstawie nazwy klasy"""
        return cls.__name__.replace('ViewSet', '').lower()

    @classmethod
    def get_actions(cls):
        """Łączy domyślne akcje z akcjami zdefiniowanymi w klasie"""
        actions = cls.default_actions.copy()
        actions.update(cls.actions)
        return actions

    @classmethod
    def create_view_handler(cls, action, action_config):
        """Tworzy handler widoku dla akcji"""

        @api_view([action_config['method']])
        def handler(request, *args, **kwargs):
            try:
                service = cls.grpc_service_class(request)
                method = getattr(service, cls.get_grpc_method_name(action))

                # Przygotuj argumenty dla metody gRPC
                if action_config['method'] in ['POST', 'PUT', 'PATCH']:
                    result = method(**request.data, **kwargs)
                else:
                    result = method(**kwargs)

                # Obsługa odpowiedzi
                if hasattr(result, cls.get_resource_name()):
                    data = {cls.get_resource_name(): ProtoSerializer(getattr(result, cls.get_resource_name())).data}
                elif hasattr(result, f"{cls.get_resource_name()}s"):
                    data = {f"{cls.get_resource_name()}s": ProtoSerializer(
                        getattr(result, f"{cls.get_resource_name()}s")).data}
                elif result is None:
                    data = {'message': 'Operation successful'}
                else:
                    data = ProtoSerializer(result).data

                return Response(data, status=200)

            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    return Response({'error': 'Resource not found'}, status=404)
                return Response({'error': e.details()}, status=500)
            except Exception as e:
                return Response({'error': str(e)}, status=500)

        return handler

    @classmethod
    def as_urls(cls):
        """Generuje URLe dla wszystkich akcji ViewSetu"""
        if not cls.grpc_service_class:
            raise ValueError(f"{cls.__name__} must define grpc_service_class")

        urls = []
        actions = cls.get_actions()

        for action, config in actions.items():
            url_pattern = f"{cls.url_prefix}/{config['url']}" if config['url'] else cls.url_prefix
            url_pattern = url_pattern.strip('/')

            urls.append(
                path(url_pattern, cls.create_view_handler(action, config))
            )

        return urls


# Przykład użycia:
class DevicesViewSet(GRPCViewSet):
    grpc_service_class = DevicesGRPCService
    url_prefix = 'devices'

    # Opcjonalnie, możesz dodać własne akcje lub nadpisać domyślne
    actions = {
        'activate': {
            'method': 'POST',
            'url': '{id}/activate',
            'grpc_method': 'activate_device'
        }
    }


# W urls.py:
urlpatterns = [
    *DevicesViewSet.as_urls()
]
