# Generated by Django 4.0.5 on 2024-04-23 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0010_alter_servies_types_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='servies_types',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
