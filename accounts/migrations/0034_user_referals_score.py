# Generated by Django 3.2.7 on 2022-06-20 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_expert_preferred_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='referals_score',
            field=models.PositiveIntegerField(default=0, verbose_name='Реферальные баллы'),
        ),
    ]
