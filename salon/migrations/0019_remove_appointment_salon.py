# Generated by Django 4.0.5 on 2024-04-25 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0018_alter_appointment_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='salon',
        ),
    ]
