from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.
class DebetCard(models.Model):
    bank_bik = models.CharField(_('БИК'), max_length=9)
    bank_name = models.CharField(_('Название банка'), max_length=255)
    bank_account = models.CharField(_('Кор счет'), max_length=255)
    bank_inn = models.CharField(_('ИНН Банка'), max_length=255)
    bank_kpp = models.CharField(_('КПП Банка'), max_length=255)
    payment_reason =  models.CharField(_('КПП Банка'), max_length=255)
    recipient_account = models.CharField(_('Р/С Получателя'), max_length=255)
    recipient_full_name =  models.CharField(_('Получатель(ФИО)'), max_length=255)
    expert = models.OneToOneField('accounts.Expert', verbose_name=_('expert'), related_name='debet_card', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = _('Дебетовая карта')
        verbose_name_plural = _('Дебетовые карты')


class BankTransaction(models.Model):
    bank_bik = models.CharField(_('БИК'), max_length=9)
    bank_name = models.CharField(_('Название банка'), max_length=255)
    bank_account = models.CharField(_('Кор счет'), max_length=255)
    bank_inn = models.CharField(_('ИНН Банка'), max_length=255)
    bank_kpp = models.CharField(_('КПП Банка'), max_length=255)
    recipient_inn =  models.CharField(_('ИНН Получателя'), max_length=255)
    recipient_name =  models.CharField(_('Наименование юр лица'), max_length=255)
    recipient_account = models.CharField(_('Р/С Получателя'), max_length=255)
    recipient_ogrn = models.CharField(_('ОГРН Получателя'), max_length=255)
    recipient_legal_address = models.CharField(_('Юр адрес'), max_length=255)
    recipient_real_address = models.CharField(_('Фактический адрес'), max_length=255)
    recipient_kpp = models.CharField(_('КПП Получателя'), max_length=255)
    recipient_status = models.CharField(_('Статус'), max_length=255)
    recipient_registration_date = models.DateField(_('Дата регистрации'), max_length=255)
    payment_reason =  models.CharField(_('КПП Банка'), max_length=255)
    expert = models.OneToOneField('accounts.Expert', on_delete=models.CASCADE, verbose_name=_('Эксперт'), related_name='scans', null=True, blank=True)
    
    class Meta:
        verbose_name = _('Банковский перевод')
        verbose_name_plural = _('Банковские переводы')


class Scan(models.Model):
    file = models.FileField(upload_to='scans')
    bank_transaction = models.ForeignKey('BankTransaction', on_delete=models.CASCADE, related_name='scans', null=True, blank=True)
    

    class Meta:
        verbose_name = _('Скан документа')
        verbose_name_plural = _('Сканы документов')
