# Generated by Django 5.1.3 on 2024-12-13 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_sprint_ended'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_teams',
        ),
        migrations.DeleteModel(
            name='ProjectTeam',
        ),
    ]
