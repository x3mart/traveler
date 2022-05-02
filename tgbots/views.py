import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import requests
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from accounts.models import User

from supports.models import SupportChatMessage, Ticket
from .models import *
from .serializers import *
from traveler.settings import TG_URL


# Create your views here.
COMMANDS_LIST = ('start', 'login', 'confirm_phone', 'create_ticket', 'cancel', 'set_to_staff', 'answer_to_user', 'proposal_to_close', 'close_ticket', 'show_last_messages', 'boss_got_new_ticket')

def get_tg_account(user):
    tg_account, created = TelegramAccount.objects.get_or_create(tg_id=user['id'])
    if created:
        user.pop('id')
        tg_account = TelegramAccount.objects.filter(pk=tg_account.id)
        tg_account.update(**user)
        tg_account = tg_account.first()
    return tg_account


@api_view(["POST", "GET"])
@permission_classes((permissions.AllowAny,))
def tg_update_handler(request):
    # response = SendMessage(chat_id=1045490278, text=request.data).send()
    # try:
    update = Update(request.data)
    if hasattr(update,'message'):
        # response = SendMessage(chat_id=1045490278, text=request.data).send()
        response = update.message_dispatcher()
    elif hasattr(update,'callback_query'):
        update.callback_dispatcher()
        # method = "sendMessage"
        # send_message = SendMessage(chat_id=1045490278, text=f'{request.data}')
        # data = SendMessageSerializer(send_message).data
        # requests.post(TG_URL + method, data)
    # except:
    #    response2 = SendMessage(chat_id=1045490278, text='response').send()
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

    def message_dispatcher(self):
        if hasattr(self.message, 'text'):
            command, args = self.command_handler(self.message.text)
        else:
            command = None
            args = []
            self.message.text = None
        self.tg_account = get_tg_account(self.message.user)
        if self.tg_account.await_reply:
            response = self.await_dispatcher(self.message.text, command, args)
        elif command:
            # response = SendMessage(chat_id=1045490278, text=command).send()
            response = self.command_dispatcher(command, args)
        else:
            text = "No commands in message"
            response = SendMessage(chat_id=self.message.chat.id, text=text).send()
            # response = None
        return response
    
    def callback_dispatcher(self):
        command, args = self.command_handler(self.callback_query.data)
        self.tg_account = get_tg_account(self.callback_query.user)
        response = self.callback_query.answer()
        if command:
            response = self.command_dispatcher(command, args)
        else:
            text = "No commands in callback_query"
            response = SendMessage(chat_id=self.message.chat.id, text=text).send()
            # response = None
        return response
    
    def command_handler(self, text):
        command = ''
        if text.startswith('/'):
            command_message = text.split(' ')
            command = command_message.pop(0).replace('/', '')
        if command in COMMANDS_LIST:
                return (command, command_message)
        else:
            return (None, [])

    def get_chat(self, source=None):
        if hasattr(self, 'callback_query'):
            chat_id=self.callback_query.message.chat.id
        else:
            chat_id=self.message.chat.id
        return chat_id
    
    def get_message(self,source=None):
        if hasattr(self, 'callback_query'):
            message=self.callback_query.message
        else:
            message=self.message
        return message
    
    def command_dispatcher(self, command, args=[]):
        chat_id = self.get_chat()
        message = self.get_message()
        kwargs = {}
        if command == 'start':
            if self.tg_account.account:
                text = render_to_string('start_for_auth.html', {'account': self.tg_account.account})
            else:
                text = render_to_string('start.html', {})
            reply_markup = ReplyMarkup().get_markup(command, self.tg_account)
            response = SendMessage(chat_id, text, reply_markup).send()
        elif command == 'login':
            self.tg_account.await_reply = True
            self.tg_account.reply_type = 'email'
            self.tg_account.save()
            response = SendMessage(chat_id, 'Введите email').send()
        elif command == 'confirm_phone':
            reply_markup = JSONRenderer().render({
                'one_time_keyboard': True,
                'keyboard':[[{'text':'Отправить номер телефона', 'request_contact':True}],
                [{'text':'Отмена'}]]
                })
            response = SendMessage(chat_id, 'Если Ваш номер телефона указанный на сайте привязан к этому аккаунту Telegram - нажмите "Отправить номер телефона"', reply_markup).send()
            self.tg_account.await_reply = True
            self.tg_account.reply_type = 'phone'
            self.tg_account.save()
        elif command == 'create_ticket' and hasattr(self.tg_account.account, 'expert'):
            self.tg_account.await_reply = True
            self.tg_account.reply_type = 'create_ticket'
            self.tg_account.save()
            text = 'Опишите Вашу проблему.'
            reply_markup = ReplyMarkup().get_markup(command, self.tg_account)
            response = SendMessage(chat_id, text, reply_markup).send()
        elif command == 'cancel' and self.tg_account.await_reply and self.tg_account.reply_type == 'create_ticket':
            self.tg_account.await_reply = False
            self.tg_account.reply_type = None
            self.tg_account.save()
            reply_markup = ReplyMarkup().get_markup('start', self.tg_account)
            response = SendMessage(chat_id, 'Заявка отменена', reply_markup).send()
        elif command == 'set_to_staff':
            ticket = Ticket.objects.get(pk=int(args[1]))
            staff = User.objects.get(pk=int(args[0]))
            user = ticket.user
            ticket.staff = staff
            ticket.status = 2
            ticket.save()
            response = SendMessage(user.telegram_account.tg_id, 'Заявка ушла в работу. Наш сотрудник ответит в ближайшее время').send()
            messages = SupportChatMessage.objects.filter(ticket=ticket)
            messages.update(reciever=staff)
            response = SendMessage(staff.telegram_account.tg_id, f'Вам назначена заявка №{ticket.id} от {user.full_name}').send()
            for chat_message in messages:
                response = SendMessage(staff.telegram_account.tg_id, chat_message.text).send()
            reply_markup = ReplyMarkup(ticket).get_markup('answer_to_user', self.tg_account)
            response = SendMessage(staff.telegram_account.tg_id, f'{user.full_name} очень ждет вашего ответа', reply_markup).send()
        elif command == 'answer_to_user':
            ticket = Ticket.objects.get(pk=int(args[0]))
            response = SendMessage(ticket.staff.telegram_account.tg_id, f'Введите сообщение для пользователя {ticket.user.full_name}').send()
            self.tg_account.await_reply = True
            self.tg_account.reply_type = 'answering'
            self.tg_account.reply_1 = ticket.id
            self.tg_account.save()
        elif command == 'boss_got_new_ticket':
            ticket = Ticket.objects.get(pk=args[0])
            reply_markup = ReplyMarkup(ticket).get_markup(command, self.tg_account)
            response = SendMessage(self.tg_account.tg_id, f'Кого назначим на заявку №{ticket.id} от пользователя {ticket.user.full_name}?', reply_markup).send()
        elif command == 'close_ticket':
            ticket = Ticket.objects.get(pk=int(args[0]))
            ticket.user.telegram_account.await_reply = False
            ticket.user.telegram_account.reply_type = None
            ticket.user.telegram_account.reply_1 = None
            ticket.user.telegram_account.save()
            ticket.status = 3
            ticket.save()
            reply_markup = ReplyMarkup().get_markup('start', ticket.user.telegram_account)
            response = SendMessage(ticket.user.telegram_account.tg_id, f'Заявка №{ticket.id} закрыта', reply_markup).send()
            reply_markup = ReplyMarkup().get_markup('start', ticket.staff.telegram_account)
            response = SendMessage(ticket.staff.telegram_account, f'Заявка №{ticket.id} закрыта', reply_markup).send()
        elif command == 'show_last_messages':
            ticket = Ticket.objects.get(pk=int(args[0]))
            messages = SupportChatMessage.objects.filter(ticket=ticket).order_by('id')
            for chat_message in messages:
                text = render_to_string('message_from.html', {'message':chat_message})
                response = SendMessage(chat_id, text).send()
            reply_markup = ReplyMarkup(ticket).get_markup('answer_to_user', self.tg_account)
            response = SendMessage(chat_id, 'Будем отвечать или закроем?', reply_markup).send()
        else:
            response = None
        return response
    
    def await_dispatcher(self, text=None, command=None, args=None):
        chat_id = self.get_chat()
        message = self.get_message()
        if self.tg_account.reply_type =='email':
            self.tg_account.reply_type = 'password'
            self.tg_account.reply_1 = text.strip()
            self.tg_account.save()
            response = SendMessage(chat_id=self.message.chat.id, text='Введите пароль').send()
        elif self.tg_account.reply_type =='password':
            account = authenticate(email=self.tg_account.reply_1, password=text.strip())
            reply_markup = ReplyMarkup().get_markup('start', self.tg_account)
            if account is not None:
                self.tg_account.account = account
                text = render_to_string('start_for_auth.html', {'account': account})
                reply_markup = ReplyMarkup().get_markup('start', self.tg_account)
                response = SendMessage(chat_id=self.message.chat.id, text=text, reply_markup=reply_markup).send()
                response = requests.post(TG_URL + 'deleteMessage', data={'chat_id':self.message.chat.id, 'message_id': self.message.message_id})
            else:
                response = SendMessage(chat_id=self.message.chat.id, text='Учетные данные не верны', reply_markup=reply_markup).send()
            self.tg_account.await_reply = False
            self.tg_account.reply_type = None
            self.tg_account.reply_1 = None
            self.tg_account.save()
        elif self.tg_account.reply_type =='phone':
            self.tg_account.await_reply = False
            self.tg_account.reply_type = None
            self.tg_account.save()
            if hasattr(message, 'text') and message.text == 'Отмена':
                text='Действие отменено'
            elif self.tg_account.account.phone and str(self.tg_account.account.phone).lstrip('+') == message.contact['phone_number'].lstrip('+'):
                self.tg_account.account.expert.phone_confirmed = True
                self.tg_account.account.expert.save()
                text='Номер телефона подтвержден'
            else:
                text='Номера телефонов не совпадают'
            reply_markup = ReplyMarkup().get_markup('start', self.tg_account)
            response = SendMessage(self.message.chat.id, text, reply_markup).send()
        elif self.tg_account.reply_type =='create_ticket':
            ticket = Ticket.objects.create(user=self.tg_account.account.expert, tg_chat=chat_id)
            chat_message = SupportChatMessage.objects.create(sender=self.tg_account.account.expert, tg_message=message.message_id, sender_chat_id=chat_id, text=message.text, ticket=ticket)
            self.tg_account.reply_type ='ticket'
            self.tg_account.save()
            text = render_to_string('ticket_created.html', {'ticket':ticket})
            response = SendMessage(chat_id, text).send()
            bosses = TelegramAccount.objects.filter(account__groups__name='support_boss')
            text = render_to_string('boss_new_ticket.html', {'ticket':ticket})
            for boss in bosses:
                reply_markup = ReplyMarkup(ticket=ticket).get_markup('boss_got_new_ticket', self.tg_account)
                response = SendMessage(boss.tg_id, text, reply_markup).send()                
        elif self.tg_account.reply_type =='ticket' and not command:
            ticket = Ticket.objects.filter(user_id=self.tg_account.account_id).filter(status__in=[1,2]).order_by('-id').first()
            chat_message = SupportChatMessage.objects.create(sender=self.tg_account.account.expert, tg_message=message.message_id, sender_chat_id=chat_id, text=message.text, ticket_id=ticket.id)
            if ticket.staff:
                chat_message.reciever = ticket.staff
                chat_message.save()
                reply_markup = ReplyMarkup(ticket).get_markup('answer_to_user', self.tg_account)
                text = render_to_string('message_from_user.html', {'ticket':ticket, 'message':message})
                response = SendMessage(ticket.staff.telegram_account.tg_id, text, reply_markup).send()
            else:
                response = None
        elif self.tg_account.reply_type =='answering' and not command:
            ticket = Ticket.objects.get(pk=int(self.tg_account.reply_1))
            chat_message = SupportChatMessage.objects.create(sender=self.tg_account.account, tg_message=message.message_id, sender_chat_id=chat_id, text=message.text, ticket_id=ticket.id, reciever=ticket.user)
            reply_markup = ReplyMarkup(ticket).get_markup('answer_to_staff', self.tg_account)
            text = render_to_string('message_from_staff.html', {'ticket':ticket, 'message':message})
            response = SendMessage(ticket.user.telegram_account.tg_id, text, reply_markup).send()
            self.tg_account.await_reply = False
            self.tg_account.reply_type = None
            self.tg_account.reply_1 = None
            self.tg_account.save()
        else:
            response = self.command_dispatcher(command, args) if command else None 
            self.tg_account.await_reply = False
            self.tg_account.reply_1 = None
            self.tg_account.reply_type = None
            self.tg_account.save()    
        return response


class CallbackQuery():
    def __init__(self, data) -> None:
        for key, value in data.items():
            if key == 'message':
                self.__setattr__(key, Message(value))
            elif key == 'from':
                self.__setattr__('user', value)
            else:
                self.__setattr__(key, value)
    
    def answer(self, text=None, show_alert=None):
        answer = AnswerCallbackQuery(callback_query_id=self.id, text=text, show_alert=show_alert)
        data = AnswerCallbackQuerySerializer(answer).data
        response = requests.post(TG_URL + 'answerCallbackQuery', data)
        return response


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


class ReplyMarkup():
    def __init__(self, ticket=None):
        self.ticket = ticket

    def get_markup(self, name, tg_account=None, **kwargs):
        if name == 'start' and tg_account and tg_account.account and hasattr(tg_account.account, 'expert') and tg_account.account.expert.phone_confirmed:
            button1 = InlineButton(text='Создать заявку', callback_data=f'/create_ticket')
            keyboard = [[button1]]
        elif name == 'start' and tg_account and tg_account.account and hasattr(tg_account.account, 'expert') and not tg_account.account.expert.phone_confirmed:
            button1 = InlineButton(text='Подтвердить телефон', callback_data=f'/confirm_phone')
            button2 = InlineButton(text='Создать заявку', callback_data=f'/create_ticket')
            keyboard = [[button1],[button2]]
        elif name == 'start' and tg_account and tg_account.account and tg_account.account.groups.filter(name='support_boss'):
            new_tickets = Ticket.objects.filter(status__in=[1])
            open_tickets = Ticket.objects.filter(status__in=[2]).filter(staff=tg_account.account)
            keyboard = []
            for ticket in new_tickets:
                button = InlineButton(text=f'Новая аявка №{ticket.id}', callback_data=f'/boss_got_new_ticket {ticket.id}')
                keyboard.append([button])
            for ticket in open_tickets:
                button = InlineButton(text=f'Открытая заявка №{ticket.id}', callback_data=f'/show_last_messages {ticket.id}')
                keyboard.append([button])
        elif name == 'create_ticket':
            button1 = InlineButton(text='Отменить', callback_data=f'/cancel')
            keyboard = [[button1]]
        elif name == 'boss_got_new_ticket':
            staffs = User.objects.filter(groups__name='support_staff')
            keyboard = []
            for staff in staffs:
                button = InlineButton(text=f'{staff.full_name}', callback_data=f'/set_to_staff {staff.id} {self.ticket.id}')
                keyboard.append([button])
        elif name == 'answer_to_user':
            button1 = InlineButton(text=f'Ответить пользователю {self.ticket.user.full_name}', callback_data=f'/answer_to_user {self.ticket.id}')
            button2 = InlineButton(text=f'Закрыть заявку №{self.ticket.id}', callback_data=f'/close_ticket {self.ticket.id}')
            keyboard = [[button1], [button2]]
        elif name == 'answer_to_staff':
            button = InlineButton(text=f'Закрыть заявку №{self.ticket.id}', callback_data=f'/close_ticket {self.ticket.id}')
            keyboard = [[button]]
        else:
            button1 = InlineButton(text='Авторизация', callback_data=f'/login')
            keyboard = [[button1]]
        
        self.inline_keyboard = keyboard
        reply_markup_data = ReplyMarkupSerializer(self).data
        return JSONRenderer().render(reply_markup_data)

