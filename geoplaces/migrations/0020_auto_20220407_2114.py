# Generated by Django 3.2.7 on 2022-04-07 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoplaces', '0019_city_search_vector_en_idx'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='city',
            name='search_vector_idx',
        ),
        migrations.RemoveIndex(
            model_name='city',
            name='search_vector_en_idx',
        ),
    ]
