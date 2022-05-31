from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.db.models import F
from tours.models import Tour
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from supports.serializers import SupportChatMessageSerializer


# def check_password(self):
#     request = self.context['request']
#     re_password = request.data.get('re_password')
#     password = request.data.get('password')
#     if not password:
#         raise serializers.ValidationError(_('Укажите пароль'))
#     if password != re_password:
#         raise serializers.ValidationError(_('Пароли должны совпадать'))
#     try:
#         validators.validate_password(password)
#     except exceptions.ValidationError as exc:
#         raise serializers.ValidationError(str(exc))
#     return password


def important_to_know():
    tours = Tour.objects.annotate(important=F('important_to_know')).filter(important_gt=0)
    for tour in tours:
        pass

class ChatMixins():
    def send_message_to_support_chat(self, chat_message, ticket):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'supportchat_{ticket.id}',
            {
                'type': 'chat_message',
                'message': SupportChatMessageSerializer(chat_message, many=False).data
            }
        ) 
    
    def send_command_to_support_chat(self, command, ticket):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'supportchat_{ticket.id}',
            {
                'type': 'chat_message',
                'command': command
            }
        ) 
    
    def send_status_to_support_chat(self, ticket):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'supportchat_{ticket.id}',
            {
                'type': 'chat_message',
                'ticket_status_changed': ticket.status
            }
        ) 

    def send_new_chat_notification(self, user, chat):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notification_{user.id}',
            {
                'type': 'chat_message',
                'new_chat': chat
            }
        )  
