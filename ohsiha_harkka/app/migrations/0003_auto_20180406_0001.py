# Generated by Django 2.0.4 on 2018-04-05 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_trafficlight_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trafficlight',
            name='last_updated',
            field=models.TextField(blank=True, null=True),
        ),
    ]
