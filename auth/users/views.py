from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
