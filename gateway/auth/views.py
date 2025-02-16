from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, RegistrationSerializer
import requests


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
        original_first_login = user.first_login
        if user.first_login:
            user.first_login = False
            user.save()
        serializer = UserSerializer(user)
        response_data = serializer.data
        response_data['first_login'] = original_first_login
        return Response(response_data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[AllowAny],
        url_path='google-userinfo',
    )
    def google_userinfo(self, request):
        """
        Handle Google user authentication and creation/update.
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"error": "Authorization header missing or invalid."}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        try:
            google_response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {token}'}
            )
            if google_response.status_code != 200:
                return Response({"error": "Invalid Google token."}, status=status.HTTP_403_FORBIDDEN)

            user_data = google_response.json()
            email = user_data.get('email')
            if not email:
                return Response({"error": "Email not available in Google response."},
                                status=status.HTTP_400_BAD_REQUEST)

            user, created = get_user_model().objects.get_or_create(email=email, defaults={
                'metadata': {'google_id': user_data.get('id')},
                'full_name': user_data.get('name'),
                'picture': user_data.get('picture'),
                'auth_type': 'google',
                'first_login': True,
            })
            original_first_login = user.first_login
            if not created:
                if user.first_login:
                    user.first_login = False
                    user.save()

            serializer = UserSerializer(user)
            response_data = serializer.data
            response_data['first_login'] = original_first_login
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Failed to authenticate with Google."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
