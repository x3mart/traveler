# Generated by Django 3.2.7 on 2021-11-16 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0015_tourbasic_wallpaper'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourbasic',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2, verbose_name='Рейтинг'),
        ),
    ]
