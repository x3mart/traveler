from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class VerificationRequest(models.Model):
    tour_operator_license = models.BooleanField(default=False)
    had_commercial_tours  = models.BooleanField(default=False)
    citizenship = models.ForeignKey('geoplaces.Country', verbose_name=_('Резидент'), on_delete=models.PROTECT)
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
