from django.contrib import admin

from supports.models import SupportChatMessage, Ticket

# Register your models here.
admin.site.register(Ticket)
admin.site.register(SupportChatMessage)