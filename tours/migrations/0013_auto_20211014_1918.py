# Generated by Django 3.2.7 on 2021-10-14 16:18

from django.db import migrations, models
import tours.models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0012_auto_20211014_1855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tourbasic',
            name='moderation',
        ),
        migrations.AddField(
            model_name='tourbasic',
            name='on_moderation',
            field=models.BooleanField(default=False, verbose_name='На модерации'),
        ),
        migrations.AddField(
            model_name='tourtype',
            name='alt',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='alt текст'),
        ),
        migrations.AddField(
            model_name='tourtype',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=tours.models.tour_types_path, verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='tourbasic',
            name='is_draft',
            field=models.BooleanField(default=True, verbose_name='Черновик'),
        ),
    ]
