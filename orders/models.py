from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
def get_order_id():
    pass

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING_CONFIRMATION = 'pending_confirmation', _('Ожидает подтверждения')
        PENDING_PREPAYMENT = 'pending_prepayment', _('Ожидает_предоплаты')
        PREPAYMENT_OVERDUE = 'prepayment_overdue', _('Предоплата просрочена')
        PREPAYMENT = 'prepayment', _('Предоплата внесена')
        FULLPAYMENT = 'fullpayment', _('Оплачено полностью')
        
    customer = models.ForeignKey('accounts.Customer', on_delete=models.PROTECT, related_name='customers_orders', verbose_name=_('Покупатель'))
    expert = models.ForeignKey('accounts.Expert', on_delete=models.PROTECT, related_name='experts_orders', verbose_name=_('Эксперт'))
    tour_id =  models.BigIntegerField(_('ID Тура'))
    tour_name = models.CharField(_('Название тура'), max_length=255)
    tour_start_date = models.DateField(_('Дата начала'))
    tour_finish_date = models.DateField(_('Дата завершения'))
    tour_price = models.PositiveIntegerField(_('Цена за место'))
    travelers_number = models.PositiveIntegerField(_('Количево участников'))
    cost = models.PositiveIntegerField(_('Стоимость тура'))
    postpay_final_date = models.DateField(_('Дата постоплаты'))
    status = models.CharField(_('Статус'), max_length=25, choices=OrderStatus.choices, default=OrderStatus.PENDING_CONFIRMATION)
    difficulty_level = models.PositiveIntegerField(_('Уровень сложности'))
    comfort_level = models.PositiveIntegerField(_('Уровень комфорта'))
    tour_excluded_services = models.JSONField(_("Не включенные услуги"))
    tour_included_services = models.JSONField(_("Включенные услуги"))
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        ordering = ['id']


class Traveler(models.Model):
    last_name = models.CharField(_('Фамилия'), max_length=50)   
    middle_name = models.CharField(_('Отчество'), max_length=50)   
    first_name = models.CharField(_('Имя'), max_length=50)
    birth_date = models.DateField(_('Дата рождения'))
    order = models.ForeignKey('Order', on_delete=models.PROTECT, related_name='travelers', verbose_name=_('Заказ'))

    class Meta:
        verbose_name = _('Путешественник')
        verbose_name_plural = _('Путешественники')
        ordering = ['id']

class FirstTraveler(Traveler):
    phone = PhoneNumberField(_('Номер телефона'))

    class Meta:
        verbose_name = _('Главный Путешественник')
        verbose_name_plural = _('Главные Путешественники')
        ordering = ['id']