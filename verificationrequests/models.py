from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class VerificationRequest(models.Model):
    TOURS_NUMBER = [
        (1, 'до 5'),
        (2, '5-12'),
        (3, '13-20'),
        (4, '21-30'),
        (5, '30+'),
    ]
    tour_operator_license = models.BooleanField(default=False)
    had_commercial_tours  = models.BooleanField(default=False)
    number_tours_per_year = models.PositiveIntegerField(_('Туры в год'), choices=TOURS_NUMBER, null=True, blank=True,)
    countries = models.ManyToManyField('geoplaces.Country', verbose_name=_('В какие страны туры'))
    other_sites = models.TextField(_('Ссылки на ресурсы'), null=True, blank=True,)
    had_conflicts  = models.BooleanField(_('Были конфликты?'), default=False)
    about_conflict = models.TextField(_('Описание конфликта'), null=True, blank=True,)
    citizenship = models.ForeignKey('geoplaces.Country', verbose_name=_('Резидент'), on_delete=models.PROTECT, related_name="%(app_label)s_%(class)s_citizenship")
    expert = models.ForeignKey('accounts.Expert', verbose_name=_('Эксперт'), on_delete=models.PROTECT)
    aproved = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Individual(VerificationRequest):
    first_name = models.CharField(_('Имя'), max_length=255)
    last_name = models.CharField(_('Фамилия'), max_length=255)
    patronymic = models.CharField(_('Отчество'), max_length=255, null=True, blank=True,)
    passport_series = models.PositiveIntegerField(_("Паспорт серия"))
    passport_number = models.PositiveIntegerField(_("Паспорт номер"))
    passport_code_issued_by = models.CharField(_('Паспорт код подразделения'), max_length=25,)
    passport_issued_by = models.CharField(_('Паспорт кем выдан'), max_length=255,)
    passport_date = models.DateField(_('Паспорт дата выдачи'))

    class Meta:
        verbose_name = _('Запрос на проверку физ лицо')
        verbose_name_plural = _('Запросы на проверку физ лицо')


class Legal(VerificationRequest):
    recipient_inn =  models.CharField(_('ИНН Получателя'), max_length=255)
    recipient_ogrn = models.CharField(_('ОГРН Получателя'), max_length=255)
    recipient_legal_address = models.CharField(_('Юр адрес'), max_length=255)
    recipient_real_address = models.CharField(_('Фактический адрес'), max_length=255)
    
    
    class Meta:
        verbose_name = _('Запрос на проверку юр лицо')
        verbose_name_plural = _('Запросы на проверку юр лицо')


class Scan(models.Model):
    file = models.FileField(upload_to='scans')
    legal = models.ForeignKey('Legal', on_delete=models.CASCADE, verbose_name=_('Запрос на проверку юр лица'), related_name='scans')
