# Generated by Django 3.2.7 on 2021-12-23 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0022_auto_20211223_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='touradvanced',
            name='duration',
            field=models.DurationField(blank=True, null=True, verbose_name='Продолжительность тура в днях'),
        ),
    ]
