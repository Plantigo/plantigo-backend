from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, RegistrationSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )
    def userinfo(self, request):
        """
        Retrieve info about the current authenticated user based on user_id from JWT token.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    A view that provides the ability to obtain a new JWT token pair.
    """

    permission_classes = [AllowAny]


class CustomTokenRefreshView(TokenRefreshView):
    """
    A view that provides the ability to refresh an existing JWT token.
    """

    pass


class RegistrationView(APIView):
    """
    A view that allows new users to register.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
