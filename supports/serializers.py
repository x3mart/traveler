from django.utils import timezone
from rest_framework import serializers

from .models import SupportChatMessage, Ticket
from accounts.models import User


class MessageAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'avatar', 'is_online')


class SupportChatMessageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    author = MessageAuthorSerializer(many=False, read_only=True)
    class Meta:
        model = SupportChatMessage
        fields = '__all__'
    
    def get_created_at(self, obj):
        if (timezone.now() - obj.created_at).days <= 0:
            return obj.created_at.strftime('%H:%M')
        return obj.created_at.strftime('%d-%m-%Y %H:%M')


class TicketSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    class Meta:
        model = Ticket
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}
    
    def get_last_message(self, obj):
        last_message = obj.ticket_messages.last()
        if last_message:
            return last_message.text
        return None

class TicketRetrieveSerializer(serializers.ModelSerializer):
    ticket_messages = SupportChatMessageSerializer(many=True, read_only=False)
    class Meta:
        model = Ticket
        exclude = '__all__'

