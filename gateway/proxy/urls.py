from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.get_devices, name='device-list'),
    path('devices/create/', views.create_device, name='device-create'),
]
