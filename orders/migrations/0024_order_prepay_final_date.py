# Generated by Django 3.2.7 on 2022-06-19 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='prepay_final_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата предоплаты'),
        ),
    ]
