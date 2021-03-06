# Generated by Django 3.2.7 on 2022-07-06 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geoplaces', '0026_auto_20220705_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='Просмотры')),
                ('country', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='geoplaces.country', verbose_name='Страна')),
                ('country_region', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='geoplaces.countryregion', verbose_name='Регион страны')),
            ],
            options={
                'verbose_name': 'Направление',
                'verbose_name_plural': 'Направления',
            },
        ),
    ]
