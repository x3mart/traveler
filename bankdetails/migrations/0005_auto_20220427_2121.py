# Generated by Django 3.2.7 on 2022-04-27 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankdetails', '0004_auto_20220427_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransaction',
            name='bank_bik',
            field=models.CharField(max_length=9, verbose_name='БИК'),
        ),
        migrations.AlterField(
            model_name='debetcard',
            name='bank_bik',
            field=models.CharField(max_length=9, verbose_name='БИК'),
        ),
    ]
