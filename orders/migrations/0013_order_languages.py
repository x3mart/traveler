# Generated by Django 3.2.7 on 2022-06-14 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_rename_tour_id_order_tour'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='languages',
            field=models.JSONField(blank=True, null=True, verbose_name='Языки'),
        ),
    ]
