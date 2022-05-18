from rest_framework import serializers

from .models import UserChat
from accounts.models import User

class RoomMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'is_online')

class UserChatSerializer(serializers.ModelSerializer):
    room_members = RoomMembersSerializer(many=True, read_only=True)
    class Meta:
        model = UserChat
        fields = '__all__'