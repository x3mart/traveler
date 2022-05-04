from django.contrib import admin

from supports.models import SupportChatMessage, Ticket
from accounts.models import User

# Register your models here.
class TiketAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'staff', 'status', 'created_at', 'accepted_at', 'closed_at') 
    list_filter = ('user', 'staff', 'status',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'staff':
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        elif db_field.name == 'staff':
            kwargs["queryset"] = User.objects.exclude(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Ticket, TiketAdmin)
admin.site.register(SupportChatMessage)