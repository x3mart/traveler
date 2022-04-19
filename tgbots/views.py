from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import *


# Create your views here.
@api_view(["POST", "GET"])
@permission_classes((permissions.AllowAny,))
def tg_update_handler(request):
    # response = SendMessage(chat_id=1045490278, text='update').send()
    try:
        update = Update(request.data)
        if hasattr(update,'message'):
            # response = SendMessage(chat_id=1045490278, text='message').send()
            update.message_dispatcher()
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
                self.__setattr__(key, Message(value))
            elif key == 'callback_query':
                self.__setattr__(key, CallbackQuery(value))
            else:
                self.__setattr__(key, value)


class CallbackQuery():
    def __init__(self, data) -> None:
        for key, value in data.items():
            if key == 'message':
                self.__setattr__(key, Message(value))
            elif key == 'from':
                self.__setattr__('user', value)
            else:
                self.__setattr__(key, value)