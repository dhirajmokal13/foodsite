# Generated by Django 4.0.5 on 2024-04-22 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0002_business_salon_address_alter_business_salon_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='salon_location',
            field=models.CharField(default='', max_length=100),
        ),
    ]