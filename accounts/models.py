from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.template.defaultfilters import slugify
from unidecode import unidecode
import os

# Create your models here.
def user_avatar_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'avatars/{0}/{1}{2}'.format(slugify(unidecode(instance.name)), slugify(unidecode(name)), extension)

class AccountManager(BaseUserManager):
    def create_user(self, email, name, password=None, is_staff=False):
        if not email:
            raise ValueError(_('Укажите Ваш e-mail'))
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            is_staff=is_staff
            )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            is_staff = True,
            is_superuser = True,
            is_active = True
            )
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, verbose_name='Полное Имя', null=True, blank=True,)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    is_expert = models.BooleanField(default=False, verbose_name='Эксперт')
    is_customer = models.BooleanField(default=False, verbose_name='Покупатель')
    phone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон')

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS =['name',]

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['id']

    def __str__(self):
        return self.name
    
    def delete(self, using=None, keep_parents=False):
        storage = self.avatar.storage
        if storage.exists(self.avatar.name):
                storage.delete(self.avatar.name)
        super().delete()