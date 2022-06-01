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
from django.utils import timezone

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
    patronymic = models.CharField(_('Отчество'), max_length=255, null=True, blank=True,)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(_('Сотрудник'), default=False, )
    is_expert = models.BooleanField(_('Эксперт'), default=False, )
    is_customer = models.BooleanField(_('Покупатель'), default=False, )
    is_online = models.BooleanField(_('Сейчас на сайте'), default=False, )
    registration_date = models.DateField(_('Дата регистрации'), auto_now_add=True, null=True, blank=True,)
    last_visit = models.DateTimeField(_('Последнее посещение'), default=timezone.now)
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
        first = self.first_name if self.first_name else '--'
        last = self.last_name if self.last_name else ''
        return f'{first} {last}'
    
    @property
    def tmb_avatar(self):
        return get_tmb_path(self.avatar.url) if self.avatar else None

    def __str__(self):
        return self.full_name
    
    
class Expert(User):
    class PreferredPaymantMethod(models.IntegerChoices):
        CARD = 1, _('Дебетовая карта')
        BANK = 2, _('Банковский перевод')

    country = models.CharField(_('Страна'), max_length=100, null=True, blank=True)
    city  = models.CharField(_('Город'), max_length=100, null=True, blank=True)
    languages = models.ManyToManyField("languages.Language" ,verbose_name=_('Языки'), blank=True, related_name='expert')
    visited_countries = models.CharField(_('Посещенные страны'), max_length=255, null=True, blank=True)
    about = RichTextField(_('О себе'), null=True, blank=True)
    video = models.URLField(_('Ссылка на видео'), max_length=255, null=True, blank=True)
    commission = models.PositiveIntegerField(_('Комиссия'), default=15)
    email_confirmed = models.BooleanField(_('Email подтвержден'), default=False)
    phone_confirmed = models.BooleanField(_('Телефон подтвержден'), default=False)
    docs_confirmed = models.BooleanField(_('Документы подтверждены'), default=False)
    status_confirmed = models.BooleanField(_('Статус подтвержден'), default=False)
    rating = models.DecimalField(_('Рейтинг'), decimal_places=1, max_digits=2, default=0)
    tours_count = models.IntegerField(_('Кол-во туров'), default=0)
    tours_rating = models.DecimalField(_('Рейтинг туров'), decimal_places=1, max_digits=2, default=0)
    reviews_count = models.IntegerField(_('Кол-во отзывов'), default=0)
    tour_reviews_count = models.IntegerField(_('Кол-во отзывов о турах'), default=0)
    # preferred_payment_method = models.IntegerField(_('Способ выплаты'), default=1, choices=PreferredPaymantMethod.choices)

    class Meta:
        verbose_name = _('Эксперт')
        verbose_name_plural = _('Эксперты')
        ordering = ['-id']

class TeamMember(models.Model):
    first_name = models.CharField(_('Имя'), max_length=255,  null=True, blank=True,)
    midle_name = models.CharField(_('Имя'), max_length=255,  null=True, blank=True,)
    last_name = models.CharField(_('Фамилия'), max_length=255, null=True, blank=True,)
    email = models.EmailField(_('email'), max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True,)
    phone = PhoneNumberField(_('Телефон'), null=True, blank=True, )
    about = models.TextField(_('О себе'), null=True, blank=True)
    expert = models.ForeignKey('Expert', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Эксперт'), related_name='team_members')
    is_active = models.BooleanField(default=True)
    is_expert = models.BooleanField(default=False)


    class Meta:
        verbose_name = _('Член команды')
        verbose_name_plural = _('Члены команды')
        ordering = ['-id', 'expert']
    
    @property
    def full_name(self):
        first = self.first_name if self.first_name else '--'
        last = self.last_name if self.last_name else ''
        return f'{first} {last}'
    
    @property
    def tmb_avatar(self):
        return get_tmb_path(self.avatar.url) if self.avatar else None
    
    def __str__(self):
        return self.full_name


class Customer(User):
    class Meta:
        verbose_name = _('Покупатели')
        verbose_name_plural = _('Покупатель')


class PhoneConfirm(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='phone_confirms')
    code = models.CharField(max_length=4)