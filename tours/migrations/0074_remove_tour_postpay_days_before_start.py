# Generated by Django 3.2.7 on 2022-04-22 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0073_auto_20220413_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='postpay_days_before_start',
        ),
    ]
