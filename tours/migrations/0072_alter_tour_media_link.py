# Generated by Django 3.2.7 on 2022-04-13 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0071_alter_tour_completed_sections'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='media_link',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка на видео тура'),
        ),
    ]
