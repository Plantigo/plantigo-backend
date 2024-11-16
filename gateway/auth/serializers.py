from django.contrib.auth import get_user_model
from django_grpc_framework import proto_serializers
from rest_framework import serializers
from grpc_interfaces.users import users_pb2


class UserProtoSerializer(proto_serializers.ModelProtoSerializer):
    """
    Serializer for the User model using gRPC.
    """

    class Meta:
        model = get_user_model()
        proto_class = users_pb2.CustomUser
        fields = ['id', 'username', 'email', 'groups']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'groups']
