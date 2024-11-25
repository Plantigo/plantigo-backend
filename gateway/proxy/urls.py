from django.urls import path
from . import views

urlpatterns = [
    path('telemetry/<str:mac_address>/period/', views.get_data_for_period, name='telemetry-period'),
    path('telemetry/<str:mac_address>/avg/', views.get_average_data, name='telemetry-avg'),
    path('telemetry/<str:mac_address>/last/', views.get_last_record, name='telemetry-last'),
    path('devices/', views.get_devices, name='device-list'),
    path('devices/create/', views.create_device, name='device-create'),
    path('devices/<str:device_id>/update/', views.update_device, name='device-update'),
    path('devices/<str:device_id>/delete/', views.delete_device, name='device-delete'),
]
