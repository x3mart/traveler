# Generated by Django 3.2.7 on 2022-02-13 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geoplaces', '0008_alter_city_russian_region'),
        ('tours', '0030_auto_20220211_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='finish_russian_region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tours_by_finish_russian_region', to='geoplaces.russianregion', verbose_name='Российский регион завершения путешествия'),
        ),
        migrations.AddField(
            model_name='tour',
            name='start_russian_region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tours_by_start_russian_region', to='geoplaces.russianregion', verbose_name='Российский регион начала путешествия'),
        ),
    ]
