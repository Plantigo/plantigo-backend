from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
import requests


class GoogleAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class for handling Google OAuth2 tokens.
    Verifies the token with Google's userinfo endpoint and returns the corresponding user.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        
        if len(token.split('.')) == 3:
            return None
            
        try:
            google_response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if google_response.status_code != 200:
                raise exceptions.AuthenticationFailed('Invalid Google token')

            user_data = google_response.json()
            email = user_data.get('email')
            
            if not email:
                raise exceptions.AuthenticationFailed('Email not available in Google response')

            User = get_user_model()
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'metadata': {'google_id': user_data.get('id')},
                    'full_name': user_data.get('name'),
                    'picture': user_data.get('picture'),
                    'auth_type': 'google',
                    'first_login': True,
                }
            )

            if not created and user.first_login:
                user.first_login = False
                user.save()

            return (user, None)

        except requests.RequestException:
            raise exceptions.AuthenticationFailed('Failed to authenticate with Google')
            