# Generated by Django 3.2.7 on 2022-07-05 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoplaces', '0025_auto_20220511_0423'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='countryregion',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='region',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]
