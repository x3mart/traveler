# Generated by Django 3.2.7 on 2022-03-31 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0064_auto_20220329_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='postpay_days_before_start',
            field=models.PositiveIntegerField(default=3, verbose_name='Дни внесения полной суммы до старта'),
        ),
    ]
