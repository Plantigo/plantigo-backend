# Generated by Django 5.1.2 on 2025-01-11 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0006_customuser_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='customuser',
            name='picture',
            field=models.URLField(blank=True),
        ),
    ]
