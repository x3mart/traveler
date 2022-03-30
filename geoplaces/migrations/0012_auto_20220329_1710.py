# Generated by Django 3.2.7 on 2022-03-29 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geoplaces', '0011_delete_russianregion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='russian_region',
        ),
        migrations.AddField(
            model_name='city',
            name='country_region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='geoplaces.countryregion', verbose_name='Регион Страны'),
        ),
    ]