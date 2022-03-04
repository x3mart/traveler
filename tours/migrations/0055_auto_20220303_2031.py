# Generated by Django 3.2.7 on 2022-03-03 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0054_auto_20220303_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='tour_addetional_services',
        ),
        migrations.AddField(
            model_name='tour',
            name='tour_addetional_services',
            field=models.JSONField(blank=True, null=True, verbose_name='Дополнительные услуги'),
        ),
        migrations.RemoveField(
            model_name='tour',
            name='tour_days',
        ),
        migrations.AddField(
            model_name='tour',
            name='tour_days',
            field=models.JSONField(blank=True, null=True, verbose_name='Дни тура'),
        ),
    ]