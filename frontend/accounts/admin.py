from accounts.models import User
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

class UserAdmin(TranslationAdmin):
    pass

admin.site.register(User, UserAdmin)