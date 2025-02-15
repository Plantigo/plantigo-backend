from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from core.models import BaseModel
from devices.models import Device, Telemetry

User = get_user_model()


class UserNotification(BaseModel):
    """
    Model for storing user notifications about sensor limit violations.
    """
    SEVERITY_CHOICES = [
        ('info', _('Information')),
        ('warning', _('Warning')),
        ('critical', _('Critical')),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text=_("User who should receive this notification")
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text=_("Device that triggered this notification")
    )
    telemetry = models.ForeignKey(
        Telemetry,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text=_("Telemetry reading that triggered this notification")
    )
    message = models.TextField(
        help_text=_("Notification message describing the violation")
    )
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='warning',
        help_text=_("Severity level of the notification")
    )
    is_read = models.BooleanField(
        default=False,
        help_text=_("Whether the notification has been read by the user")
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When the notification was read by the user")
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['device', '-created_at']),
            models.Index(fields=['is_read', '-created_at']),
        ]

    def __str__(self) -> str:
        return f"Notification for {self.user.username} - {self.device.name}"

    def mark_as_read(self) -> None:
        """Mark the notification as read and save the timestamp."""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
