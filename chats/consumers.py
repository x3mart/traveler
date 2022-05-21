import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.forms.models import model_to_dict
# from accounts.models import User
from chats.models import ChatMessage, UserChat
from chats.serializers import ChatMessageSerializer

class ChatConsumer(WebsocketConsumer):


    def get_chat(self):
        return UserChat.objects.get(pk=self.room_name)
    

    def get_old_messages(self):
        print('0')
        print('suki')
        print(self.room_name)
        messages = ChatMessage.objects.filter(room=int(self.room_name)).order_by('created_at')
        print('1,5')
        print(messages)
        messages = ChatMessageSerializer(messages, many=True).data
        print('11')
        return messages

    
    def save_message(self, message):
        message = ChatMessage.objects.create(room=self.chat, author=self.user, text=message)
        return ChatMessageSerializer(message, many=False).data
        
    

    def set_online_status_member_in_room(self, online=False):
        if online:
            self.chat.members_in_room.add(self.user)
        else:
            self.chat.members_in_room.remove(self.user)
    

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']
        self.chat = self.get_chat()
        self.set_online_status_member_in_room(online=True)

        # Join room group
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        print('2')
        # messages = self.get_old_messages()
        # print(messages)
        # for message in messages:
        #     self.send(text_data=json.dumps({
        #     'message': message['text'],
        #     'created_at': message['created_at'],
        #     'author': message['author']
        #     }))
        print('3')
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': 'Wellcome'
        #     }
        # )
        

    def disconnect(self, close_code):
        self.set_online_status_member_in_room(online=False)
        # await self.channel_layer.group_send(
        #     'chat_notify',
        #     {
        #         'type': 'chat_message',
        #         'message': 'Diconect'
        #     }
        # )
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )
        
        message = self.save_message(message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        message = self.save_message(message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message['text'],
            'created_at': message['created_at'],
            'author': message['author']
        }))