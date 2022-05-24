# Generated by Django 3.2.7 on 2022-05-24 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('supports', '0007_alter_ticket_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportchatmessage',
            name='reciever',
        ),
        migrations.RemoveField(
            model_name='supportchatmessage',
            name='sender',
        ),
        migrations.AddField(
            model_name='supportchatmessage',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='support_chat_messages', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель'),
        ),
        migrations.AddField(
            model_name='supportchatmessage',
            name='is_read',
            field=models.BooleanField(default=True, verbose_name='Прочитано'),
        ),
        migrations.AlterField(
            model_name='supportchatmessage',
            name='sender_chat_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='id tg чата отправителя'),
        ),
        migrations.AlterField(
            model_name='supportchatmessage',
            name='tg_message',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='id tg сообщения'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='tg_chat',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='id tg чата'),
        ),
    ]
