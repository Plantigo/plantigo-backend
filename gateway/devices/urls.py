from rest_framework.routers import DefaultRouter

from .views import DeviceViewSet, TelemetryViewSet

router = DefaultRouter()
router.register('devices', DeviceViewSet, basename='device')
router.register('telemetry', TelemetryViewSet, basename='telemetry')

urlpatterns = router.urls 