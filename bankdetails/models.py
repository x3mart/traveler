from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.
class Bank(models.Model):
    bank_bik = models.CharField(_('БИК'), max_length=255)
    bank_name = models.CharField(_('Название банка'), max_length=255)
    bank_account = models.CharField(_('Кор счет'), max_length=255)
    bank_inn = models.CharField(_('ИНН Банка'), max_length=255)
    bank_kpp = models.CharField(_('КПП Банка'), max_length=255)
    bank_payment_reason =  models.CharField(_('КПП Банка'), max_length=255)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.expert.full_name


class DebetCard(Bank):
    recipient_full_name =  models.CharField(_('Получатель(ФИО)'), max_length=255)
    expert = models.OneToOneField('accounts.Expert', verbose_name=_('expert'), related_name='debet_card', on_delete=models.PROTECT, null=True, blank=True)


    class Meta:
        verbose_name = _('Дебетовая карта')
        verbose_name_plural = _('Дебетовые карты')


class BankTransaction(Bank):
    recipient_inn =  models.CharField(_('ИНН Получателя'), max_length=255)
    recipient_account = models.CharField(_('Р/С Получателя'), max_length=255)
    recipient_registration_date = models.DateField(_('Дата регистрации'), max_length=255)
    recipient_ogrn = models.CharField(_('ОГРН Получателя'), max_length=255)
    recipient_kpp = models.CharField(_('КПП Получателя'), max_length=255, blank=True, null=True)
    recipient_status = models.CharField(_('Статус'), max_length=255)
    recipient_registration_date = models.DateField(_('Дата регистрации'), max_length=255, blank=True, null=True)
    expert = models.OneToOneField('accounts.Expert', verbose_name=_('expert'), related_name='bank_transaction', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = _('Банковский перевод')
        verbose_name_plural = _('Банковские переводы')

