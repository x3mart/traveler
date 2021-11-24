# Generated by Django 3.2.7 on 2021-11-24 12:34

from django.db import migrations, models
import tours.models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0019_tourbasic_reviews_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourday',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=tours.models.tour_image_path, verbose_name='Фото'),
        ),
    ]
