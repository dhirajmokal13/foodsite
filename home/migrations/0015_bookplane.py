# Generated by Django 4.0.4 on 2022-05-10 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_delete_bookplane'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookplane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('uname', models.CharField(max_length=20)),
                ('buname', models.CharField(max_length=20)),
                ('pid', models.IntegerField()),
                ('pname', models.CharField(max_length=150)),
                ('p_end', models.DateField()),
                ('address', models.TextField()),
                ('no_weeks', models.IntegerField()),
                ('total_amount', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
    ]
