import math
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from datetime import date
from django.db.models import F
from tours.models import Tour
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from supports.serializers import SupportChatMessageSerializer
from .constants import *
from .prices import get_tour_discounted_price, get_tour_book_price, get_tour_daily_price


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


class TourSerializerMixin():
    
    def get_start_time(self, obj):
        if obj.start_time:
            return obj.start_time.strftime('%H:%M')
        else:
            return None

    def get_finish_time(self, obj):
        if obj.finish_time:
            return obj.finish_time.strftime('%H:%M')
        else:
            return None
    
    def get_discounted_price(self, obj):
        return get_tour_discounted_price(obj)

    def get_book_price(self, obj): 
        return get_tour_book_price(obj)
    
    def get_daily_price(self, obj):
        return get_tour_daily_price(obj)

    def get_vacants_number(self, obj):
            return obj.vacants_number if obj.vacants_number < 5 else None
        
    def get_is_favourite(self, obj):
        return  None

    def get_is_new(self, obj):
        return  None

    def get_is_recomended(self, obj):
        return  None

    def get_discount(self, obj):
        return get_tour_discounted_price(obj)

    def get_main_impressions(self, obj):
        if obj.main_impressions:
            return '; '.join(obj.main_impressions)
        else:
            return ""
    def get_tour_included_services(self, obj): 
        if obj.tour_included_services:
            return '; '.join(obj.tour_included_services)
        else:
            return ""
    
    def get_tour_excluded_services(self, obj):
        if obj.tour_excluded_services is not None:
            return '; '.join(obj.tour_excluded_services)
        else:
            return "" 
    
    def get_required_fields(self, obj):
        required_fields = []
        for value in TOUR_REQUIRED_FIELDS:
            required_fields += TOUR_REQUIRED_FIELDS[value]
        return required_fields
    
    def get_postpay_days_before_start(self, obj):
        return obj.postpay_days_before_start.days
    
    def get_postpay_final_date(self, obj):
        return (obj.start_date - obj.postpay_days_before_start).strftime('%d.%m.%Y')
