from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('auth.urls')),
    path('api/v1/', include('devices.urls')),
    path('api/v1/', include('notifications.urls')),
    # path('api/v1/', include('proxy.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
