# Generated by Django 3.2.7 on 2021-11-24 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20211124_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='tour_reviews_count',
            field=models.IntegerField(default=0, verbose_name='Кол-во отзывов о турах'),
        ),
    ]
