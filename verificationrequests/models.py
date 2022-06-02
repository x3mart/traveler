from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class VerificationRequest(models.Model):
    class YesNoChoices(models.TextChoices):
        YES = 'yes', _('Да')
        NO = 'no', _('Нет')

    first_name = models.CharField(_('Имя'), max_length=255)
    last_name = models.CharField(_('Фамилия'), max_length=255)
    patronymic = models.CharField(_('Отчество'), max_length=255)
    passport_series = models.CharField(_("Паспорт серия"), max_length=255)
    passport_number = models.CharField(_("Паспорт номер"), max_length=255)
    passport_code_issued_by = models.CharField(_('Паспорт код подразделения'), max_length=25,)
    passport_issued_by = models.CharField(_('Паспорт кем выдан'), max_length=255,)
    passport_date = models.DateField(_('Паспорт дата выдачи'))
    expert = models.OneToOneField('accounts.Expert', verbose_name=_('Эксперт'), on_delete=models.PROTECT, related_name='verifications')
    # residency = models.ForeignKey('geoplaces.Country', verbose_name=_('Резидент'), on_delete=models.PROTECT, related_name="%(app_label)s_%(class)s_citizenship", null=True, blank=True,)
    license = models.CharField(_('Наличие лицензии'), max_length=3, choices=YesNoChoices.choices, default=YesNoChoices.YES)
    commercial_tours  = models.CharField(_('Коммерческие туры'), max_length=3, choices=YesNoChoices.choices, default=YesNoChoices.YES)
    # commercial_tours_yearly = models.CharField(_('Туры в год'), max_length=6, null=True, blank=True,)
    reviews_links = models.TextField(_('Ссылки на отзывы'), null=True, blank=True,)
    tours_countries = models.ManyToManyField('geoplaces.Country', verbose_name=_('В какие страны туры'), blank=True,)
    tours_links = models.TextField(_('Ссылки на туры'), null=True, blank=True,)
    conflicts  = models.TextField(_('Были конфликты?'), max_length=3, choices=YesNoChoices.choices, default=YesNoChoices.NO)
    conflicts_review = models.TextField(_('Описание конфликта'), null=True, blank=True,)
    legal_restrictions  = models.CharField(_('Были конфликты?'), max_length=3, choices=YesNoChoices.choices, default=YesNoChoices.YES)
    legal_restrictions_review = models.TextField(_('Описание конфликта'), null=True, blank=True,)
    aproved = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Запрос на проверку')
        verbose_name_plural = _('Запросы на проверку')
