# Generated by Django 3.2.7 on 2022-02-27 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0045_auto_20220227_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='sold',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Продажи'),
        ),
        migrations.AddField(
            model_name='tour',
            name='watched',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Просмотры'),
        ),
    ]
