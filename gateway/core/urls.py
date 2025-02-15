from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth.urls')),
    path('api/', include('devices.urls')),
    path('api/', include('notifications.urls')),
    # path('api/v1/', include('proxy.urls')),
]
