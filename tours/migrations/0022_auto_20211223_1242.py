# Generated by Django 3.2.7 on 2021-12-23 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0021_auto_20211222_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='touradvanced',
            name='cost',
            field=models.IntegerField(blank=True, null=True, verbose_name='Стоимость со скидкой'),
        ),
        migrations.AddField(
            model_name='touradvanced',
            name='discount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Скидка'),
        ),
    ]
