# Generated by Django 3.2.7 on 2021-11-24 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0018_auto_20211117_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourbasic',
            name='reviews_count',
            field=models.IntegerField(default=0, verbose_name='Кол-во отзывов'),
        ),
    ]