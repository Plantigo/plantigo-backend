# Generated by Django 5.1.2 on 2024-12-29 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_remove_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_login',
            field=models.BooleanField(default=True),
        ),
    ]
