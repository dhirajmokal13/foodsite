# Generated by Django 4.0.4 on 2022-05-10 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_bookplane'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookplane',
            name='p_end',
            field=models.TextField(),
        ),
    ]
