# Generated by Django 3.2.7 on 2022-02-27 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0042_tourbasic_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='direct_link',
        ),
        migrations.AddField(
            model_name='tourbasic',
            name='direct_link',
            field=models.BooleanField(default=False, verbose_name='Доступ по прямой ссылке'),
        ),
    ]
