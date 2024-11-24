from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.get_devices, name='device-list'),
    path('devices/create/', views.create_device, name='device-create'),
    path('devices/<str:device_id>/update/', views.update_device, name='device-update'),
    path('devices/<str:device_id>/delete/', views.delete_device, name='device-delete'),
]
