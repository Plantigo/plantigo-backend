import uuid
from django.db import models
from django.utils.timezone import now

from core.managers import BaseModelManager


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)
    is_deleted = models.BooleanField(default=False)

    objects = BaseModelManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True
   