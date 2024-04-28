# Generated by Django 4.0.4 on 2022-05-10 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_delete_bookplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookplan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('uname', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('no_weeks', models.IntegerField()),
                ('total_amount', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
    ]
