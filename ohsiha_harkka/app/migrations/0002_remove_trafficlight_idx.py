# Generated by Django 2.0.4 on 2018-04-05 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trafficlight',
            name='idx',
        ),
    ]