# Generated by Django 3.2.7 on 2022-05-31 19:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_auto_20220531_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 19, 30, 48, 926742), verbose_name='Последнее посещение'),
        ),
        migrations.AlterField(
            model_name='user',
            name='registration_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата регистрации'),
        ),
    ]