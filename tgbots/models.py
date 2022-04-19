from django.db import models

# Create your models here.
class TelegramAccount(models.Model):
    tg_id = models.BigIntegerField(unique=True)
    is_bot = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    language_code = models.CharField(max_length=255, null=True, blank=True)
    is_auth = models.BooleanField(default=False)
    account = models.OneToOneField('accounts.User', on_delete=models.PROTECT, related_name='telegram_account', null=True, blank=True)
    notofication = models.BooleanField(default=False)
    await_reply = models.BooleanField(default=False)
    reply_type = models.CharField(max_length=255, null=True, blank=True)
    reply_1 = models.TextField(null=True, blank=True)
    reply_2 = models.TextField(null=True, blank=True)
    reply_3 = models.TextField(null=True, blank=True)
    reply_4 = models.TextField(null=True, blank=True)
    reply_5 = models.TextField(null=True, blank=True)
    reply_6 = models.TextField(null=True, blank=True)
    reply_7 = models.TextField(null=True, blank=True)
    reply_8 = models.TextField(null=True, blank=True)
    reply_9 = models.TextField(null=True, blank=True)
    reply_10 = models.TextField(null=True, blank=True)

    # def __str__(self) -> str:
    #     return self.username

class AnswerCallbackQuery():
    def __init__(self, text, url=None, callback_query_id=None, show_alert=False, cache_time=0):
        self.text = text
        self.show_alert = show_alert
        self.callback_query_id = callback_query_id
        self.cache_time = cache_time
        if url:
            self.url = url

class InlineButton:
    def __init__(self, text, url=None, callback_data=None, login_url=None, switch_inline_query=None):
        self.text = text
        self.login_url = login_url
        self.callback_data = callback_data
        self.switch_inline_query = switch_inline_query
        if url:
            self.url = url


class KeyboardButton():
    def __init__(self, text, request_contact=None, request_location=None, request_poll=None):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll



class TgUser():
    def __init__(self, data) -> None:
        for key, value in data.items():
            self.__setattr__(key, value)


class Chat():
    def __init__(self, data) -> None:
        for key, value in data.items():
            self.__setattr__(key, value)


class Message():
    def __init__(self, data):
        for key, value in data.items():
            if key == 'reply_to_message':
                self.__setattr__(key, Message(value))
            elif key == 'from':
                self.__setattr__('user', value)
            elif key == 'chat':
                self.__setattr__(key, Chat(value))
            else:
                self.__setattr__(key, value)