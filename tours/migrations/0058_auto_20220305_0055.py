# Generated by Django 3.2.7 on 2022-03-04 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_customer_options'),
        ('tours', '0057_tourguestguideimage_expert'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tourdayimage',
            name='alt',
        ),
        migrations.RemoveField(
            model_name='tourimage',
            name='alt',
        ),
        migrations.RemoveField(
            model_name='tourimage',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tourimage',
            name='name',
        ),
        migrations.RemoveField(
            model_name='tourpropertyimage',
            name='alt',
        ),
        migrations.RemoveField(
            model_name='tourpropertyimage',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tourpropertyimage',
            name='name',
        ),
        migrations.AddField(
            model_name='tourdayimage',
            name='expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tour_day_images', to='accounts.expert'),
        ),
        migrations.AddField(
            model_name='tourdayimage',
            name='tour_basic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tour_day_images', to='tours.tourbasic', verbose_name='Основа тура'),
        ),
        migrations.AddField(
            model_name='tourimage',
            name='expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tour_images', to='accounts.expert'),
        ),
        migrations.AddField(
            model_name='tourimage',
            name='tour_basic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tour_images', to='tours.tourbasic', verbose_name='Основа тура'),
        ),
        migrations.AddField(
            model_name='tourplanimage',
            name='expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tour_plan_images', to='accounts.expert'),
        ),
        migrations.AddField(
            model_name='tourplanimage',
            name='tour_basic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tour_plan_images', to='tours.tourbasic', verbose_name='Основа тура'),
        ),
        migrations.AddField(
            model_name='tourpropertyimage',
            name='expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tour_property_images', to='accounts.expert'),
        ),
        migrations.AddField(
            model_name='tourpropertyimage',
            name='tour_basic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tour_property_images', to='tours.tourbasic', verbose_name='Основа тура'),
        ),
        migrations.DeleteModel(
            name='TourDay',
        ),
    ]
