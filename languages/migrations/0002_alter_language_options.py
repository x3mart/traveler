# Generated by Django 3.2.7 on 2021-10-14 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='language',
            options={'verbose_name': 'Язык', 'verbose_name_plural': 'Языки'},
        ),
    ]
