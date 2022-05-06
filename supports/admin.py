from django.contrib import admin
from django.utils.safestring import mark_safe
from supports.models import SupportChatMessage, Ticket
from accounts.models import User

# Register your models here.
class TicketMessageInline(admin.TabularInline):
    model = SupportChatMessage
    fields = ('text',)
    readonly_fields = ('text',)
    extra = 0
    can_delete = False
    show_change_link = False

    def get_max_num(self, request, obj=None, **kwargs):
        return obj.ticket_messages.count()
class TiketAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'staff', 'status_colored', 'created_at', 'accepted_at', 'closed_at') 
    list_filter = (('staff', admin.RelatedOnlyFieldListFilter), ('user', admin.RelatedOnlyFieldListFilter), 'status',)
    ordering = ['status', '-created_at']
    inlines = [
        TicketMessageInline,
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'staff':
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        elif db_field.name == 'user':
            kwargs["queryset"] = User.objects.exclude(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def status_colored(self, obj):
        if obj.status == 1:
            return mark_safe('<b style="color:{};">{}</b>'.format('red', obj.get_status_display()))
        if obj.status == 2:
            status = '<b style="color:{};">{}</b>'.format('orange', obj.get_status_display())
        elif obj.status == 3:
            status = '<b style="color:{};">{}</b>'.format('green', obj.get_status_display())
        return mark_safe(status)

    status_colored.short_description = 'Статус'
    



admin.site.register(Ticket, TiketAdmin)
# admin.site.register(SupportChatMessage)