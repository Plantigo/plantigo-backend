import logging
from concurrent import futures

import grpc
from plantigo_common.grpc.auth_interceptor import AuthInterceptor

from core.settings import settings


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         interceptors=[AuthInterceptor(settings.jwt_secret_key, settings.jwt_algorithm)])
    server.add_insecure_port("{}:{}".format(settings.app_host, settings.app_port))
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
