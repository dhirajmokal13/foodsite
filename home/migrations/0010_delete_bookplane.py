# Generated by Django 4.0.4 on 2022-05-10 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_rename_bookplan_bookplane'),
    ]

    operations = [
        migrations.DeleteModel(
            name='bookplane',
        ),
    ]