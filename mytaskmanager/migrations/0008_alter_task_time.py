# Generated by Django 5.1.6 on 2025-03-19 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytaskmanager', '0007_task_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
