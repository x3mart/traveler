from django.contrib import admin

from supports.models import SupportChatMessage, Ticket

# Register your models here.
class TiketAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_staff')


admin.site.register(Ticket)
admin.site.register(SupportChatMessage)