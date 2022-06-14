# Generated by Django 3.2.7 on 2022-06-14 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20220614_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='postpay_final_date',
            field=models.CharField(max_length=25, verbose_name='Дата постоплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='tour_finish_date',
            field=models.CharField(max_length=25, verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='tour_start_date',
            field=models.CharField(max_length=25, verbose_name='Дата начала'),
        ),
    ]
