# Generated by Django 3.2.7 on 2022-07-05 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0081_declinereason_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tourtype',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='age_ends',
            field=models.PositiveIntegerField(blank=True, default=85, null=True, verbose_name='Макс возраст участника тура'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='name',
            field=models.CharField(blank=True, max_length=180, null=True, verbose_name='Название'),
        ),
    ]
