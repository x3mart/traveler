from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UserChat(models.Model):
    # room_name = models.CharField(_('Название комнаты'), max_length=255)
    room_members = models.ManyToManyField('accounts.User', related_name='chat_rooms')
    members_in_room = models.ManyToManyField('accounts.User', related_name='user_in_rooms')

    class Meta:
        verbose_name = _('Чат')
        verbose_name_plural = _('Чаты')
    
    def __str__(self) -> str:
        return f'{self.room_members.first().full_name} - {self.room_members.last().full_name}'


class ChatMessage(models.Model):
    room = models.ForeignKey('UserChat', on_delete=models.CASCADE, related_name='room_messages')
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_chat_messages')
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # class Meta:
    #     ordering = ['-created_at']