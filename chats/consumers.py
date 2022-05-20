import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.forms.models import model_to_dict
# from accounts.models import User
from chats.models import ChatMessage, UserChat
from chats.serializers import ChatMessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_chat(self):
        return UserChat.objects.get(pk=self.room_name)
    
    @database_sync_to_async
    def get_old_messages(self):
        messages = ChatMessage.objects.filter(room=self.room_name)
        return ChatMessageSerializer(messages, many=True).data
    
    @database_sync_to_async
    def save_message(self, message):
        ChatMessage.objects.create(room=self.chat, author=self.user, text=message)
    
    @database_sync_to_async
    def set_online_status_member_in_room(self, online=False):
        if online:
            self.chat.members_in_room.add(self.user)
        else:
            self.chat.members_in_room.remove(self.user)
    

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']
        self.chat = await self.get_chat()
        await self.set_online_status_member_in_room(online=True)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': 'Wellcome'
        #     }
        # )

        # await self.send(text_data=json.dumps({
        #     'message':'',
        #     'old_messages': await self.get_old_messages()
        # }))

    async def disconnect(self, close_code):
        await self.set_online_status_member_in_room(online=False)
        # await self.channel_layer.group_send(
        #     'chat_notify',
        #     {
        #         'type': 'chat_message',
        #         'message': 'Diconect'
        #     }
        # )
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        await self.save_message(message)


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))