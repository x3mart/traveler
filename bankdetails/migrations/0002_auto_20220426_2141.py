# Generated by Django 3.2.7 on 2022-04-26 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankdetails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransaction',
            name='recipient_kpp',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='КПП Получателя'),
        ),
        migrations.AlterField(
            model_name='banktransaction',
            name='recipient_registration_date',
            field=models.DateField(blank=True, max_length=255, null=True, verbose_name='Дата регистрации'),
        ),
    ]
