from pyexpat import model
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Ticket(models.Model):
    stuff = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name=_('Сотрудник'), related_name='stuff_chats', null=True, blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name=_('Пользователь'), related_name='user_chats')
    tg_chat = models.BigIntegerField(_('id tg чата'))
    created_at = models.DateTimeField(_('Создана'), auto_now_add=True)
    


class ChatMessage(models.Model):
    sender = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name=_('Отправитель'), related_name='sender_messages', null=True, blank=True)
    reciever = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name=_('Получатель'), related_name='reciever_messages', null=True, blank=True)
    tg_message = models.BigIntegerField(_('id tg сообщения'))
    sender_chat_id = models.BigIntegerField(_('id tg сообщения'), null=True, blank=True)
    text = models.TextField(_('Текст'), null=True, blank=True)
    ticket = models.ForeignKey('Ticket', on_delete=models.PROTECT, verbose_name=_('Заявка'), related_name='ticket_messages')
    created_at = models.DateTimeField(_('Создана'), auto_now_add=True)