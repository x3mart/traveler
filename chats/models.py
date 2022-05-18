from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UserChat(models.Model):
    # room_name = models.CharField(_('Название комнаты'), max_length=255)
    room_members = models.ManyToManyField('accounts.User', related_name='chat_rooms')
    members_in_room = models.ManyToManyField('accounts.User', related_name='user_in_rooms')


class ChatMessage(models.Model):
    room = models.ForeignKey('UserChat', on_delete=models.CASCADE, related_name='room_messages')
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_chat_messages')
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']