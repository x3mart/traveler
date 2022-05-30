from django.contrib import admin

from chats.models import ChatMessage, UserChat

# Register your models here.
class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    fields = ('text',)
    readonly_fields = ('text',)
    extra = 0
    can_delete = False
    show_change_link = False

    def get_max_num(self, request, obj=None, **kwargs):
        return obj.room_messages.count()


class UserChatAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fieldsets = ((None, {}),)
    inlines = [
        ChatMessageInline,
    ]


admin.site.register(UserChat, UserChatAdmin)
admin.site.register(ChatMessage)