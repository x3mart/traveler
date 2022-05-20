from datetime import datetime
from rest_framework import serializers

from .models import ChatMessage, UserChat
from accounts.models import User

class RoomMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name')

class ChatMessageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    author = RoomMembersSerializer(many=False, read_only=True)
    class Meta:
        model = ChatMessage
        fields = '__all__'
    
    def get_created_at(self, obj):
        if (datetime.now() - obj.created_at).days <= 0:
            return obj.created_at.strftime('%H:%M')
        return obj.created_at.strftime('%d-%m-%Y %H:%M')


class UserChatSerializer(serializers.ModelSerializer):
    room_members = RoomMembersSerializer(many=True, read_only=True)
    members_in_room = RoomMembersSerializer(many=True, read_only=True)
    # last_message = serializers.SerializerMethodField()
    class Meta:
        model = UserChat
        fields = '__all__'
    
    def get_last_message(self, obj):
        last_message = obj.room_messages.first()
        if last_message:
            return last_message.text
        return None