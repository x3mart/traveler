# Generated by Django 3.2.7 on 2021-12-22 10:40

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_expert_tours_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tmb_avatar',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.user_avatar_path),
        ),
    ]
