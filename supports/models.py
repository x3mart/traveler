from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Ticket(models.Model):
    STATUSES = (
        (1, 'Открыта'),
        (2, 'В работе'),
        (3, 'Закрыта'),
    )
    staff = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name=_('Сотрудник'), related_name='staff_chats', null=True, blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name=_('Пользователь'), related_name='user_chats')
    status = models.PositiveIntegerField(_('Статус'), default=1, choices=STATUSES)
    tg_chat = models.BigIntegerField(_('id tg чата'), null=True, blank=True)
    created_at = models.DateTimeField(_('Создана'), auto_now_add=True)
    accepted_at = models.DateTimeField(_('Ушла в работу'), null=True, blank=True)
    closed_at = models.DateTimeField(_('Закрыта в'), null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка в ТП'
        verbose_name_plural = 'Заявки в ТП'
        ordering = ['status', '-created_at']
    
    def __str__(self):
        return f'Заявка №{self.id}'
        
    

class SupportChatMessage(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name=_('Отправитель'), related_name='support_chat_messages', null=True, blank=True)
    # receiver = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name=_('Получатель'), related_name='receiver_messages', null=True, blank=True)
    tg_message = models.BigIntegerField(_('id tg сообщения'), null=True, blank=True)
    sender_chat_id = models.BigIntegerField(_('id tg чата отправителя'), null=True, blank=True)
    text = models.TextField(_('Текст'), null=True, blank=True)
    ticket = models.ForeignKey('Ticket', on_delete=models.PROTECT, verbose_name=_('Заявка'), related_name='ticket_messages')
    created_at = models.DateTimeField(_('Создана'), auto_now_add=True)
    is_read = models.BooleanField(_("Прочитано"),default=True)

    def __str__(self):
        return f'{self.author} {self.created_at.strftime("%d.%m.%Y, %H:%M:%S")}'