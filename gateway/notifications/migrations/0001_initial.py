# Generated by Django 5.1.2 on 2025-02-15 20:53

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('devices', '0003_devicesensorlimits'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False)),
                ('message', models.TextField(help_text='Notification message describing the violation')),
                ('severity', models.CharField(choices=[('info', 'Information'), ('warning', 'Warning'), ('critical', 'Critical')], default='warning', help_text='Severity level of the notification', max_length=10)),
                ('is_read', models.BooleanField(default=False, help_text='Whether the notification has been read by the user')),
                ('read_at', models.DateTimeField(blank=True, help_text='When the notification was read by the user', null=True)),
                ('device', models.ForeignKey(help_text='Device that triggered this notification', on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='devices.device')),
                ('telemetry', models.ForeignKey(help_text='Telemetry reading that triggered this notification', on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='devices.telemetry')),
                ('user', models.ForeignKey(help_text='User who should receive this notification', on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['user', '-created_at'], name='notificatio_user_id_776dd3_idx'), models.Index(fields=['device', '-created_at'], name='notificatio_device__980f56_idx'), models.Index(fields=['is_read', '-created_at'], name='notificatio_is_read_0f6abc_idx')],
            },
        ),
    ]
