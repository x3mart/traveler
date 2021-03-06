# Generated by Django 3.2.7 on 2022-04-22 18:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0074_remove_tour_postpay_days_before_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='postpay_days_before_start',
            field=models.DurationField(blank=True, default=datetime.timedelta(days=5), null=True, verbose_name='Дни внесения полной суммы до старта'),
        ),
    ]
