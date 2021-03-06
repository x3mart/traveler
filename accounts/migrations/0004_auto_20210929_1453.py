# Generated by Django 3.2.7 on 2021-09-29 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210929_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='about_en',
            field=models.TextField(blank=True, null=True, verbose_name='О себе'),
        ),
        migrations.AddField(
            model_name='expert',
            name='about_ru',
            field=models.TextField(blank=True, null=True, verbose_name='О себе'),
        ),
        migrations.AddField(
            model_name='expert',
            name='city_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='expert',
            name='city_ru',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='expert',
            name='country_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='expert',
            name='country_ru',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='expert',
            name='languages_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Языки'),
        ),
        migrations.AddField(
            model_name='expert',
            name='languages_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Языки'),
        ),
        migrations.AddField(
            model_name='expert',
            name='visited_countries_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Посещенные страны'),
        ),
        migrations.AddField(
            model_name='expert',
            name='visited_countries_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Посещенные страны'),
        ),
    ]
