from concurrent import futures
import grpc
import logging

from auth_token.interceptor import AuthInterceptor
from devices.devices_pb2_grpc import add_DeviceServiceServicer_to_server
from devices.grpc_service import DeviceGRPCService


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[AuthInterceptor()])
    add_DeviceServiceServicer_to_server(DeviceGRPCService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info("Starting gRPC server on port [::]:50051...")
    serve()
