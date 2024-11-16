from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    A view that provides the ability to obtain a new JWT token pair.
    """
    permission_classes = [AllowAny]


class CustomTokenRefreshView(TokenRefreshView):
    """
    A view that provides the ability to refresh an existing JWT token.
    """
    permission_classes = [AllowAny]
