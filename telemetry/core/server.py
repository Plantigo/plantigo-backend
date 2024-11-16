from concurrent import futures

import grpc
from plantigo_common.grpc.auth_interceptor import AuthInterceptor

from core.database import get_collection
from core.logging import configure_logging
from core.settings import settings
from shared.dispatcher_pb2_grpc import add_DispatcherServicer_to_server
from dispatcher.service import DispatcherGRPCService


def initialize_server():
    logger = configure_logging()
    logger.info("Initializing gRPC server...")

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=settings.max_grpc_workers),
        interceptors=[AuthInterceptor(settings.jwt_secret_key, settings.jwt_algorithm)]
    )

    db_collection = get_collection(settings.iot_collection_name)
    logger.info(f"Database collection {settings.iot_collection_name} initialized.")

    add_DispatcherServicer_to_server(DispatcherGRPCService(db_collection), server)

    server_address = f"{settings.app_host}:{settings.app_port}"
    if settings.use_tls:
        with open(settings.tls_cert_path, "rb") as cert_file, open(settings.tls_key_path, "rb") as key_file:
            server_credentials = grpc.ssl_server_credentials([(key_file.read(), cert_file.read())])
        server.add_secure_port(server_address, server_credentials)
        logger.info(f"gRPC server bound securely to {server_address} (TLS enabled).")
    else:
        server.add_insecure_port(server_address)
        logger.info(f"gRPC server bound to {server_address} (TLS disabled).")

    return server, logger


def serve():
    server, logger = initialize_server()

    try:
        server.start()
        logger.info("gRPC server started.")
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.warning("Server interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        server.stop(0)
        logger.info("Database connection closed.")
        logger.info("Server stopped gracefully.")
