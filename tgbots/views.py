from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import requests
from .models import *
from .serializers import *
from traveler.settings import TG_URL


# Create your views here.
@api_view(["POST", "GET"])
@permission_classes((permissions.AllowAny,))
def tg_update_handler(request):
    # response = SendMessage(chat_id=1045490278, text='update').send()
    try:
        update = Update(request.data)
        if hasattr(update,'message'):
            response = SendMessage(chat_id=update.get_chat(), text='message').send()
            response2 = SendMessage(chat_id=1045490278, text=response).send()
            # update.message_dispatcher()
        elif hasattr(update,'callback_query'):
            update.callback_dispatcher()
        # method = "sendMessage"
        # send_message = SendMessage(chat_id=1045490278, text=f'{request.data}')
        # data = SendMessageSerializer(send_message).data
        # requests.post(TG_URL + method, data)
    except:
       pass
    return Response({}, status=200)

class Update():
    def __init__(self, data) -> None:
        for key, value in data.items():
            if key == 'message':
                print('message')
                self.__setattr__(key, Message(value))
            elif key == 'callback_query':
                self.__setattr__(key, CallbackQuery(value))
            else:
                self.__setattr__(key, value)
    
    def get_chat(self, source=None):
        if hasattr(self, 'callback_query'):
            print(self.callback_query)
            chat_id=self.callback_query.message.chat.id
        else:
            chat_id=self.message.chat.id
        return chat_id


class CallbackQuery():
    def __init__(self, data) -> None:
        for key, value in data.items():
            if key == 'message':
                self.__setattr__(key, Message(value))
            elif key == 'from':
                self.__setattr__('user', value)
            else:
                self.__setattr__(key, value)


class SendMessage():
    def __init__(self, chat_id, text=None, reply_markup=None, message_id=None, parse_mode='HTML') -> None:
        self.chat_id = chat_id
        self.text = text
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.message_id = message_id
    
    def edit_text(self):
        data = SendMessageSerializer(self).data
        response = requests.post(TG_URL + 'editMessageText', data)
        return response
    
    def edit_markup(self):
        data = SendMessageSerializer(self).data
        response = requests.post(TG_URL + 'editMessageReplyMarkup', data)
        return response

    def send(self):
        data = SendMessageSerializer(self).data
        response = requests.post(TG_URL + 'sendMessage', data)
        return response