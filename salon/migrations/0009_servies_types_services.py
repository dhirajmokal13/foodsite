# Generated by Django 4.0.5 on 2024-04-23 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0008_business_closing_time_business_open_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='servies_types',
            name='services',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='salon.services'),
        ),
    ]
