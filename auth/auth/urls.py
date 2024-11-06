from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import user_pb2_grpc
from users.services import UserService

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


def grpc_handlers(server):
    user_pb2_grpc.add_CustomUserControllerServicer_to_server(UserService.as_servicer(), server)
