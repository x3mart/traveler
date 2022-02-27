# Generated by Django 3.2.7 on 2022-02-27 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0041_auto_20220227_1456'),
        ('reviews', '0004_alter_tourreview_tour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourreview',
            name='tour',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tour_reviews', to='tours.tourbasic', verbose_name='Тур'),
        ),
    ]