# Generated by Django 5.1.3 on 2024-11-25 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_taskcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('todo', 'Todo'), ('in_progress', 'In Progress'), ('review', 'Review'), ('completed', 'Completed')], default='todo', max_length=20),
        ),
    ]
