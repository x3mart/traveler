# Generated by Django 3.2.7 on 2022-02-14 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0034_auto_20220214_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='price_comment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Коментарий к стоимости'),
        ),
    ]
