from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.template.defaultfilters import slugify
from unidecode import unidecode
import os
from traveler.settings import BASE_DIR
from ckeditor.fields import RichTextField
from utils.images import get_tmb_path

# Create your models here.
def user_avatar_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'avatars/{0}/{1}{2}'.format(slugify(unidecode(instance.full_name)), slugify(unidecode(name)), '.jpg')

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False):
        if not email:
            raise ValueError(_('Укажите Ваш e-mail'))
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff
            )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff = True,
            is_superuser = True,
            is_active = True
            )
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(_('Имя'), max_length=255,  null=True, blank=True,)
    last_name = models.CharField(_('Фамилия'), max_length=255, null=True, blank=True,)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True,)
    # tmb_avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(_('Сотрудник'), default=False, )
    is_expert = models.BooleanField(_('Эксперт'), default=False, )
    is_customer = models.BooleanField(_('Покупатель'), default=False, )
    phone = PhoneNumberField(_('Телефон'), null=True, blank=True, )

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS =['name',]

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-id']
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def tmb_avatar(self):
        if self.avatar:
            tmb_path = get_tmb_path(self.avatar.url)
            return tmb_path
        return None

    def __str__(self):
        return self.full_name
    
    
class Expert(User):
    country = models.CharField(_('Страна'), max_length=100, null=True, blank=True)
    city  = models.CharField(_('Город'), max_length=100, null=True, blank=True)
    languages = models.CharField(_('Языки'), max_length=255, null=True, blank=True)
    visited_countries = models.CharField(_('Посещенные страны'), max_length=255, null=True, blank=True)
    about = RichTextField(_('О себе'), null=True, blank=True)
    email_confirmed = models.BooleanField(_('Email подтвержден'), default=False)
    phone_confirmed = models.BooleanField(_('Телефон подтвержден'), default=False)
    docs_confirmed = models.BooleanField(_('Документы подтверждены'), default=False)
    status_confirmed = models.BooleanField(_('Статус подтвержден'), default=False)
    rating = models.DecimalField(_('Рейтинг'), decimal_places=1, max_digits=2, default=0)
    tours_count = models.IntegerField(_('Кол-во туров'), default=0)
    tours_rating = models.DecimalField(_('Рейтинг туров'), decimal_places=1, max_digits=2, default=0)
    reviews_count = models.IntegerField(_('Кол-во отзывов'), default=0)
    tour_reviews_count = models.IntegerField(_('Кол-во отзывов о турах'), default=0)

    class Meta:
        verbose_name = _('Эксперт')
        verbose_name_plural = _('Эксперты')
        ordering = ['-id']
    
    def __str__(self):
        return self.full_name


class TeamMember(models.Model):
    first_name = models.CharField(_('Имя'), max_length=255,  null=True, blank=True,)
    last_name = models.CharField(_('Фамилия'), max_length=255, null=True, blank=True,)
    email = models.EmailField(_('email'), max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True,)
    languages = models.ManyToManyField("languages.Language" ,verbose_name=_('Языки'), blank=True, related_name='team_member')
    about = models.TextField(_('О себе'), null=True, blank=True)
    expert = models.ForeignKey('Expert', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Эксперт'), related_name='team_members')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Член команды')
        verbose_name_plural = _('Члены команды')
        ordering = ['expert' ,'-id']
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def tmb_avatar(self):
        if self.avatar:
            tmb_path = get_tmb_path(self.avatar.url)
            return tmb_path
        return None
    
    def __str__(self):
        return self.full_name


class Customer(User):
    class Meta:
        verbose_name = _('Путешественник')
        verbose_name_plural = _('Путешественники')