from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import UserNotification
from .serializers import UserNotificationSerializer


class UserNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing user notifications.
    
    list:
        Get list of user's notifications
    retrieve:
        Get specific notification details
    mark_as_read:
        Mark notification as read
    mark_all_as_read:
        Mark all user's notifications as read
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationSerializer
    
    def get_queryset(self):
        return UserNotification.objects.filter(
            user=self.request.user
        ).select_related(
            'device',
            'telemetry'
        )
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark specific notification as read."""
        notification = self.get_object()
        notification.mark_as_read()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all user's unread notifications as read."""
        now = timezone.now()
        count = self.get_queryset().filter(
            is_read=False
        ).update(
            is_read=True,
            read_at=now
        )
        return Response({
            'message': f'Marked {count} notifications as read',
            'count': count
        }, status=status.HTTP_200_OK)
