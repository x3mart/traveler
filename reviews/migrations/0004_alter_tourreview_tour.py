# Generated by Django 3.2.7 on 2022-02-10 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0029_auto_20220210_1728'),
        ('reviews', '0003_alter_tourreview_tour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourreview',
            name='tour',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tour_reviews', to='tours.tour', verbose_name='Тур'),
        ),
    ]
