import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.template.loader import render_to_string
from tgbots.views import ReplyMarkup, SendMessage
from accounts.models import User
from supports.serializers import SupportChatMessageSerializer
from supports.models import SupportChatMessage, Ticket

class SupportChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_ticket(self):
        return Ticket.objects.get(pk=self.room_name)
    
    @database_sync_to_async
    def get_chatmate_status(self):
        return self.ticket.members_in_room.count() > 1
        
    @database_sync_to_async
    def get_old_messages(self):
        SupportChatMessage.objects.filter(ticket=self.ticket).exclude(author=self.user).filter(is_read=False).update(is_read=True)
        messages = SupportChatMessage.objects.filter(ticket=self.ticket).prefetch_related('author').order_by('created_at')
        return SupportChatMessageSerializer(messages, many=True).data

    @database_sync_to_async   
    def save_message(self, message):
        # is_read = True if self.chat.members_in_room.count() > 1 else False
        is_read = True if self.ticket.status == 2 else False
        message = SupportChatMessage.objects.create(ticket=self.ticket, author=self.user, text=message, is_read=is_read)
        return SupportChatMessageSerializer(message, many=False).data
        
    @database_sync_to_async
    def set_online_status_member_in_room(self, online=False):
        if online:
            self.chat.members_in_room.add(self.user)
        else:
            self.chat.members_in_room.remove(self.user)

    @sync_to_async
    def send_to_support_tg_bot(self):
        reply_markup = ReplyMarkup(self.ticket).get_markup('answer_to_user', self.user.telegram_account)
        text = render_to_string('message_from_user.html', {'ticket':self.ticket, 'message':self.message})
        SendMessage(self.ticket.staff.telegram_account.tg_id, text, reply_markup).send()
    

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'supportchat_%s' % self.room_name

        self.user = self.scope['user']
        self.ticket = await self.get_ticket()
        # await self.set_online_status_member_in_room(online=True)
        # self.chatmate_status = await self.get_chatmate_status()
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        if self.ticket.status == 2:
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
        if self.ticket.status == 2 and not self.message.author.is_staff:
            await self.send_to_support_tg_bot()
        
        
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