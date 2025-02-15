from rest_framework.routers import DefaultRouter

from .views import UserNotificationViewSet

router = DefaultRouter()
router.register('notifications', UserNotificationViewSet, basename='notification')

urlpatterns = router.urls 