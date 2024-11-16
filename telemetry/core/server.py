from concurrent import futures

import grpc
from plantigo_common.grpc.auth_interceptor import AuthInterceptor

from core.database import get_collection
from core.settings import settings
from dispatcher.dispatcher_pb2_grpc import add_DispatcherServicer_to_server
from dispatcher.service import DispatcherGRPCService

db_collection = get_collection("telemetry")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         interceptors=[AuthInterceptor(settings.jwt_secret_key, settings.jwt_algorithm)])
    add_DispatcherServicer_to_server(DispatcherGRPCService(db_collection), server)
    server.add_insecure_port("{}:{}".format(settings.app_host, settings.app_port))
    server.start()
    server.wait_for_termination()
