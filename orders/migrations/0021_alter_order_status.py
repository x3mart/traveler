# Generated by Django 3.2.7 on 2022-06-16 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_auto_20220615_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'Черновик'), ('cancelled_by_customer', 'Отменен покупателем'), ('cancelled_by_expert', 'Отменен экспертом'), ('declined', 'Отказ в бронировании'), ('form_completed', 'Форма заполнена'), ('pending_confirmation', 'Ожидает подтверждения'), ('pending_prepayment', 'Ожидает предоплаты'), ('prepayment_overdue', 'Предоплата просрочена'), ('prepayment', 'Забронирован'), ('fullpayment', 'Оплачено полностью')], default='new', max_length=25, verbose_name='Статус'),
        ),
    ]
