from django.contrib.auth.models import User
from django_grpc_framework import proto_serializers
from rest_framework import serializers
import users_pb2


class UserProtoSerializer(proto_serializers.ModelProtoSerializer):
    """
    Serializer for the User model using gRPC.
    """

    class Meta:
        model = User
        proto_class = users_pb2.User
        fields = ['id', 'username', 'email', 'groups']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']
