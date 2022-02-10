# Generated by Django 3.2.7 on 2022-02-10 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0003_auto_20220210_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='language',
            name='native_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Оригинальное название'),
        ),
    ]
