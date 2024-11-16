import grpc
from shared.devices_pb2_grpc import DeviceServiceStub
from shared import devices_pb2

GRPC_SERVICES = {
    "devices": {
        "stub": DeviceServiceStub,
        "address": "localhost:50051",
        "request_classes": {
            "GetAllDevices": devices_pb2.GetDevicesRequest,
        },
    },
}


class GRPCClient:
    def __init__(self, stub_class, address: str):
        """
        gRPC client for a specific stub.

        Args:
            stub_class: The gRPC stub class.
            address (str): The gRPC server address.
        """
        self.channel = grpc.insecure_channel(address)
        self.stub = stub_class(self.channel)

    def call_method(self, method_name: str, grpc_request, metadata: list = None):
        """
        Calls a gRPC method.

        Args:
            method_name (str): The name of the method to call.
            grpc_request: The request object for the gRPC method.
            metadata (list): Metadata headers.

        Returns:
            The response from the gRPC method.
        """
        method = getattr(self.stub, method_name, None)
        if not method:
            raise ValueError(f"Method '{method_name}' not found in stub.")
        return method(grpc_request, metadata=metadata)


class GRPCServiceFacade:

    def __init__(self, request, service_name):
        """
        Facade managing gRPC calls for a specific service.

        Args:
            request: HTTP object containing authentication data.
            service_name: Name of the service (e.g., 'devices').
        """
        self.request = request
        self.metadata = [("authorization", f"Bearer {self.request.auth.token.decode('utf-8')}")]
        self.service_name = service_name

        service_config = GRPC_SERVICES[service_name]
        self.client = GRPCClient(service_config["stub"], service_config["address"])
        self.request_classes = service_config["request_classes"]

    def call(self, method: str):
        """
        Calls a method in the gRPC service.

        Args:
            method: The name of the gRPC method.

        Returns:
            The response from the gRPC service.
        """
        if method not in self.request_classes:
            raise ValueError(f"Method '{method}' not configured for service '{self.service_name}'")

        grpc_request = self.request_classes[method]()  # Tworzenie instancji request
        return self.client.call_method(method, grpc_request, metadata=self.metadata)


class GRPCServiceFactory:
    """
    Factory creating gRPC service classes based on `GRPCServiceFacade.grpc_services`.
    """

    @staticmethod
    def create_service_class(service_name):
        """
        Creates a service class based on the name.

        Args:
            service_name: The name of the service (e.g., 'devices').

        Returns:
            A service class with methods based on gRPC methods.
        """
        facade_class = GRPCServiceFacade

        class DynamicGRPCService(facade_class):
            def __init__(self, request):
                super().__init__(request, service_name)

            def __getattr__(self, name):
                method_name = "".join(part.capitalize() for part in name.split("_"))
                if method_name in self.request_classes:
                    return lambda: self.call(method_name)
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        return DynamicGRPCService
