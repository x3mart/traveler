# Generated by Django 3.2.7 on 2022-06-02 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verificationrequests', '0012_verificationrequest_residency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verificationrequest',
            old_name='first_name',
            new_name='passport_first_name',
        ),
        migrations.RenameField(
            model_name='verificationrequest',
            old_name='last_name',
            new_name='passport_last_name',
        ),
        migrations.RenameField(
            model_name='verificationrequest',
            old_name='patronymic',
            new_name='passport_patronymic',
        ),
    ]
