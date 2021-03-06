# Generated by Django 3.2.7 on 2022-02-13 15:15

from django.db import migrations, models
import django.db.models.deletion
import geoplaces.models


class Migration(migrations.Migration):

    dependencies = [
        ('geoplaces', '0003_auto_20211014_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='RussianRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to=geoplaces.models.geo_path, verbose_name='Фото')),
                ('alt', models.CharField(blank=True, max_length=255, null=True, verbose_name='alt текст')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='geoplaces.country', verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='city',
            name='russian_region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='geoplaces.russianregion', verbose_name='Страна'),
        ),
    ]
