from accounts.models import Customer, Expert, TeamMember, User
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.safestring import mark_safe
from modeltranslation.forms import TranslationModelForm
from django import forms
from django.contrib.auth.admin import UserAdmin


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name_ru', 'last_name' , 'avatar', 'is_superuser', 'is_active')

class UserAdmin(UserAdmin, TranslationAdmin):
    add_form = UserCreationForm
    add_fieldsets = (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name_ru', 'password1', 'password2', 'avatar', 'is_superuser', 'is_active'),
        }),
    fieldsets = ((None, {'fields':('first_name', 'last_name', 'email', 'password', 'phone', 'avatar', 'is_active', 'groups')}),)
    ordering = ('-id',)
    list_display = ('email', 'full_name', 'is_superuser', 'is_staff')

    # def get_queryset(self, request):
    #     return User.objects.filter(is_staff=True)

class ExpertCreationForm(UserCreationForm):
    class Meta:
        model = Expert
        fields = ('first_name_ru', 'last_name_ru', 'email', 'phone', 'avatar')


class ExpertAdmin(UserAdmin, TranslationAdmin):
    add_form = ExpertCreationForm
    list_display = ('get_avatar', 'full_name', 'country', 'city', 'is_active', 'email_confirmed', 'phone_confirmed', 'docs_confirmed', 'status_confirmed', 'commission')
    list_editable =('is_active', 'email_confirmed', 'phone_confirmed', 'docs_confirmed', 'status_confirmed', 'commission')
    fieldsets = ((None, {'fields':('first_name', 'last_name', 'email', 'password', 'phone', 'avatar', 'country', 'city', 'is_active', 'email_confirmed', 'phone_confirmed', 'docs_confirmed', 'status_confirmed', 'visited_countries', 'languages', 'about')}),)
    add_fieldsets = ((None, {'fields':('first_name_ru', 'last_name_ru', 'email', 'password1', 'password2', 'phone', 'avatar', 'country_ru', 'city_ru', 'is_active', 'email_confirmed', 'phone_confirmed', 'docs_confirmed', 'status_confirmed', 'visited_countries_ru', 'languages_ru', 'about_ru')}),)
    list_filter = ('country', 'city', 'is_active', 'email_confirmed', 'phone_confirmed', 'docs_confirmed', 'status_confirmed', 'commission')

    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="45">')
        else:
            return '-'
    
    get_avatar.short_description = 'Аватар'

    def get_queryset(self, request):
        return Expert.objects.all()

class CustomerAdmin(UserAdmin, TranslationAdmin):
    def get_queryset(self, request):
        return Customer.objects.all()

admin.site.register(User, UserAdmin)
admin.site.register(Expert, ExpertAdmin)
admin.site.register(TeamMember)
admin.site.register(Customer, CustomerAdmin)