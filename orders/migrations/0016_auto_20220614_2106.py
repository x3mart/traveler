# Generated by Django 3.2.7 on 2022-06-14 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_traveler_index_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='currency',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Знак валюты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='finish_date',
            field=models.CharField(max_length=50, verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='postpay_final_date',
            field=models.CharField(max_length=50, verbose_name='Дата постоплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='start_date',
            field=models.CharField(max_length=50, verbose_name='Дата начала'),
        ),
    ]