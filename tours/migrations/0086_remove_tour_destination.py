# Generated by Django 3.2.7 on 2022-07-07 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0085_auto_20220707_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='destination',
        ),
    ]