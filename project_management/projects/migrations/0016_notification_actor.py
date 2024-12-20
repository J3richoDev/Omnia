# Generated by Django 5.1.3 on 2024-12-15 18:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_notification'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='actor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actor_notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
