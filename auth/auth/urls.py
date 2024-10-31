from django.contrib import admin
from django.urls import path, include
import users_pb2_grpc
from users.services import UserService

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users', include('users.urls')),
]


def grpc_handlers(server):
    users_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)
