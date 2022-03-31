# Generated by Django 3.2.7 on 2022-03-31 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0065_alter_tour_postpay_days_before_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='postpay_days_before_start',
            field=models.PositiveIntegerField(blank=True, default=3, verbose_name='Дни внесения полной суммы до старта'),
        ),
    ]