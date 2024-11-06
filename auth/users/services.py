from django.contrib.auth import get_user_model
from django_grpc_framework import generics
from users.serializers import UserProtoSerializer


class UserService(generics.ModelService):
    """
    gRPC service that allows users to be retrieved or updated.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserProtoSerializer
