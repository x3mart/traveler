# Generated by Django 3.2.7 on 2022-02-18 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0039_auto_20220218_0153'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='air_tickets',
            field=models.TextField(blank=True, null=True, verbose_name='Авиабилеты'),
        ),
    ]
