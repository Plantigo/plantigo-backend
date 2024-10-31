from django_grpc_framework.management.commands.grpcrunserver import Command as GrpcRunserverCommand


class Command(GrpcRunserverCommand):
    requires_system_checks: list = []
