from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery
from chats.serializers import UserChatSerializer
from utils.mixins import ChatMixins
from .models import ChatMessage, UserChat
from accounts.models import User

# Create your views here.
class UserChatListCreateView(generics.ListCreateAPIView, ChatMixins):
    queryset = UserChat.objects.all()
    serializer = UserChatSerializer

    def create(self, request):
        chat_with = User.objects.get(pk=request.data.get('chat_with'))
        chats = UserChat.objects.filter(room_members__id=request.user.id).filter(room_members__id=chat_with.id)
        if chats.exists():
            chat = chats.first()
        else:
            chat = UserChat.objects.create()
            chat.room_members.add(request.user, chat_with)
            self.send_new_chat_notification(chat_with, UserChatSerializer(chat, many=False, context={'user':chat_with}).data)
        return Response(UserChatSerializer(chat, context={'user':request.user}).data, status=200)
    
    def list(self, request):
        latest= ChatMessage.objects.filter(room=OuterRef('pk')).order_by('-created_at')
        chats = UserChat.objects.filter(room_members__id=request.user.id).annotate(last_message=Subquery(latest.values('text')[:1]))
        serializer = UserChatSerializer(chats, many=True, context={'user':request.user})
        return Response(serializer.data)

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

def room2(request):
    return render(request, 'chat/room2.html', {
        'room_name': 1
    })