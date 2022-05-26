from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from chats.serializers import UserChatSerializer
from .models import UserChat
from accounts.models import User

# Create your views here.
class UserChatListCreateView(generics.ListCreateAPIView):
    queryset = UserChat.objects.all()[:25]
    serializer = UserChatSerializer

    def create(self, request):
        chat_with = User.objects.get(pk=request.data.get('chat_with'))
        chats = UserChat.objects.filter(room_members__id=request.user.id).filter(room_members__id=chat_with.id)
        if chats.exists():
            chat = chats.first()
        else:
            chat = UserChat.objects.create()
            chat.room_members.add(request.user, chat_with)
        return Response(UserChatSerializer(chat, context={'request':request}).data, status=200)
    
    def list(self, request):
        chats = UserChat.objects.filter(room_members__id=request.user.id)
        serializer = UserChatSerializer(chats, many=True, context={'request':request})
        return Response(serializer.data)

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

def room2(request):
    return render(request, 'chat/room2.html', {
        'room_name': 1
    })