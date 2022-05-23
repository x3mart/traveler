import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.forms.models import model_to_dict
from accounts.models import User
from chats.models import ChatMessage, UserChat
from chats.serializers import ChatMessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_chat(self):
        return UserChat.objects.get(pk=self.room_name)
    
    @database_sync_to_async
    def get_chatmate_status(self):
        return self.chat.members_in_room.count() > 1
        
    @database_sync_to_async
    def get_old_messages(self):
        ChatMessage.objects.filter(room=int(self.room_name)).exclude(author=self.user).filter(is_read=False).update(is_read=True)
        messages = ChatMessage.objects.filter(room=int(self.room_name)).order_by('created_at')
        return ChatMessageSerializer(messages, many=True).data

    @database_sync_to_async   
    def save_message(self, message):
        is_read = True if self.chat.members_in_room.count() > 1 else False
        message = ChatMessage.objects.create(room=self.chat, author=self.user, text=message, is_read=is_read)
        return ChatMessageSerializer(message, many=False).data
        
    
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
        self.chatmate_status = await self.get_chatmate_status()
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        if self.chatmate_status:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'command': 'set_read'
                }
            )

        messages = await self.get_old_messages()
        for message in messages:
            await self.send(text_data=json.dumps({
            'message': message['text'],
            'created_at': message['created_at'],
            'author': message['author'],
            'is_read': message['is_read']
            }))
        

    async def disconnect(self, close_code):
        await self.set_online_status_member_in_room(online=False)

        await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'command': 'set_unread'
                }
            )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.message = await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': self.message
            }
        )
        
        
    # Receive message from room group
    async def chat_message(self, event):
        if event.get('message'):
            message = event['message']
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message['text'],
                'created_at': message['created_at'],
                'author': message['author'],
                'is_read': message['is_read']
            }))
        elif event.get('command'):
            # Send command to WebSocket
            await self.send(text_data=json.dumps({
                'command': event['command']
            }))


class NotificationConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def set_online_status(self, online=False):
        User.objects.filter(pk=self.user['id']).update(is_online=online)


    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.user['id']
        self.room_group_name = 'chat_%s' % self.room_name
        self.chat = await self.get_chat()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.set_online_status(online=True)
    

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name       
        )
        await self.set_online_status(online=False)
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    async def chat_message(self, event):
        if event.get('message'):
            message = event['message']
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message['text'],
                'created_at': message['created_at'],
                'author': message['author'],
                'is_read': message['is_read']
            }))
        elif event.get('command'):
            # Send command to WebSocket
            await self.send(text_data=json.dumps({
                'command': event['command']
            }))
