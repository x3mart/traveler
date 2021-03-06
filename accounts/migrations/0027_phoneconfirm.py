# Generated by Django 3.2.7 on 2022-05-02 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_user_patronymic'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneConfirm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_confirms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
