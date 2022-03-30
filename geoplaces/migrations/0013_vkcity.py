# Generated by Django 3.2.7 on 2022-03-29 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geoplaces', '0012_auto_20220329_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='VKCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('foreign_id', models.IntegerField(blank=True, null=True, verbose_name='Сторонний ключ')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vkcities', to='geoplaces.country', verbose_name='Страна')),
                ('country_region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vkcities', to='geoplaces.countryregion', verbose_name='Регион Страны')),
            ],
        ),
    ]
