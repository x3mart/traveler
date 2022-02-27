# Generated by Django 3.2.7 on 2022-02-27 14:34

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import tours.models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0044_auto_20220227_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='plan',
        ),
        migrations.CreateModel(
            name='TourPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to=tours.models.tour_image_path, verbose_name='Фото')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Описание')),
                ('tour', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plan', to='tours.tour', verbose_name='Тур')),
            ],
            options={
                'verbose_name': 'День тура',
                'verbose_name_plural': 'Дни туров',
                'ordering': ['id'],
            },
        ),
    ]