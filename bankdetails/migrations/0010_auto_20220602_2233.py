# Generated by Django 3.2.7 on 2022-06-02 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bankdetails', '0009_alter_banktransaction_expert'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banktransaction',
            old_name='bank_account',
            new_name='transaction_bank_account',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='bank_bik',
            new_name='transaction_bank_bik',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='bank_inn',
            new_name='transaction_bank_inn',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='bank_kpp',
            new_name='transaction_bank_kpp',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='bank_name',
            new_name='transaction_bank_name',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='payment_reason',
            new_name='transaction_payment_reason',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='recipient_account',
            new_name='transaction_recipient_account',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='recipient_inn',
            new_name='transaction_recipient_inn',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='recipient_kpp',
            new_name='transaction_recipient_kpp',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='recipient_legal_address',
            new_name='transaction_recipient_legal_address',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='recipient_name',
            new_name='transaction_recipient_name',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='recipient_ogrn',
            new_name='transaction_recipient_ogrn',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='recipient_real_address',
            new_name='transaction_recipient_real_address',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='recipient_registration_date',
            new_name='transaction_recipient_registration_date',
        ),
        migrations.RenameField(
            model_name='banktransaction',
            old_name='recipient_status',
            new_name='transaction_recipient_status',
        ),
        migrations.RenameField(
            model_name='debetcard',
            old_name='bank_account',
            new_name='debet_card_bank_account',
        ),
        migrations.RenameField(
            model_name='debetcard',
            old_name='bank_bik',
            new_name='debet_card_bank_bik',
        ),
        migrations.RenameField(
            model_name='debetcard',
            old_name='bank_inn',
            new_name='debet_card_bank_inn',
        ),
        migrations.RenameField(
            model_name='debetcard',
            old_name='bank_kpp',
            new_name='debet_card_bank_kpp',
        ),
        migrations.RenameField(
            model_name='debetcard',
            old_name='bank_name',
            new_name='debet_card_bank_name',
        ),
        migrations.RenameField(
            model_name='debetcard',
            old_name='payment_reason',
            new_name='debet_card_payment_reason',
        ),
        migrations.RenameField(
            model_name='debetcard',
            old_name='recipient_account',
            new_name='debet_card_recipient_account',
        ),
        migrations.RenameField(
            model_name='debetcard',
            old_name='recipient_full_name',
            new_name='debet_card_recipient_full_name',
        ),
    ]
