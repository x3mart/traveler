from django.utils import timezone
from rest_framework import serializers

from .models import ChatMessage, UserChat
from accounts.models import User
from utils.images import get_tmb_image_uri

class RoomMembersSerializer(serializers.ModelSerializer):
    # avatar = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'avatar')
    
    # def get_avatar(self, obj): 
    #     return get_tmb_image_uri(self, obj)

class ChatMessageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    author = RoomMembersSerializer(many=False, read_only=True)
    class Meta:
        model = ChatMessage
        fields = '__all__'
    
    def get_created_at(self, obj):
        if (timezone.now() - obj.created_at).days <= 0:
            return obj.created_at.strftime('%H:%M')
        return obj.created_at.strftime('%d-%m-%Y %H:%M')


class UserChatSerializer(serializers.ModelSerializer):
    room_members = serializers.SerializerMethodField()
    members_in_room = RoomMembersSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    class Meta:
        model = UserChat
        fields = '__all__'
    
    def get_last_message(self, obj):
        last_message = obj.room_messages.first()
        if last_message:
            return last_message.text
        return None
    
    def get_room_members(self, obj):
        request = self.context['request']
        return RoomMembersSerializer(obj.room_members.exclude(id=request.user.id), many=True, context={'request':request}).data