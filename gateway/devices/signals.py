from django.dispatch import receiver
from devices.models import Telemetry
from django.db.models.signals import post_save


@receiver(post_save, sender=Telemetry)
def update_device_status(sender, instance, **kwargs):
    instance.device.update_active_status()
