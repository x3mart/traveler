# Generated by Django 3.2.7 on 2021-11-24 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_expert_tour_reviews_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='tours_count',
            field=models.IntegerField(default=0, verbose_name='Кол-во туров'),
        ),
    ]