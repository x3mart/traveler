# Generated by Django 3.2.7 on 2022-04-26 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bankdetails', '0001_initial'),
        ('accounts', '0023_auto_20220426_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='bank_transaction',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='expert', to='bankdetails.banktransaction', verbose_name='Банковский перевод'),
        ),
        migrations.AddField(
            model_name='expert',
            name='debet_card',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='expert', to='bankdetails.debetcard', verbose_name='Дебетовая карта'),
        ),
    ]