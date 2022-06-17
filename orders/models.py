from email.policy import default
from locale import currency
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
def get_order_id():
    pass

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        NEW_ORDER = 'new', _('Черновик')
        CANCELLED_BY_CUSTOMER = 'cancelled_by_customer', _('Отменен покупателем')
        CANCELLED_BY_EXPERT = 'cancelled_by_expert', _('Отменен экспертом')
        DECLINED = 'declined', _('Отказ в бронировании')
        PENDING_CONFIRMATION = 'pending_confirmation', _('Ожидает подтверждения')
        PENDING_PREPAYMENT = 'pending_prepayment', _('Ожидает предоплаты')
        PREPAYMENT_OVERDUE = 'prepayment_overdue', _('Предоплата просрочена')
        PREPAYMENT = 'prepayment', _('Забронирован')
        FULLPAYMENT = 'fullpayment', _('Оплачено полностью')
        
    customer = models.ForeignKey('accounts.Customer', on_delete=models.PROTECT, related_name='customers_orders', verbose_name=_('Покупатель'))
    expert = models.ForeignKey('accounts.Expert', on_delete=models.PROTECT, related_name='experts_orders', verbose_name=_('Эксперт'))
    tour =  models.ForeignKey('tours.Tour', on_delete=models.PROTECT, related_name='tours_orders', verbose_name=_('Тур'))
    name = models.CharField(_('Название тура'), max_length=255)
    start_date = models.DateField(_('Дата начала'), null=True, blank=True)
    finish_date = models.DateField(_('Дата завершения'), null=True, blank=True)
    currency = models.CharField(_('Знак валюты'), max_length=50, null=True, blank=True)
    price = models.PositiveIntegerField(_('Цена за место'))
    travelers_number = models.PositiveIntegerField(_('Количево участников'))
    cost = models.PositiveIntegerField(_('Полная стоимость тура'), null=True, blank=True)
    book_price = models.PositiveIntegerField(_('Стоимость бронирования за место'), null=True, blank=True)
    book_cost = models.PositiveIntegerField(_('Полная стоимость бронирования тура'), null=True, blank=True)
    postpay = models.PositiveIntegerField(_('Размер постоплаты за место'), null=True, blank=True)
    full_postpay = models.PositiveIntegerField(_('Полный размер постоплаты'), null=True, blank=True)
    postpay_final_date = models.DateField(_('Дата постоплаты'), null=True, blank=True)
    status = models.CharField(_('Статус'), max_length=25, choices=OrderStatus.choices, default=OrderStatus.NEW_ORDER)
    difficulty_level = models.PositiveIntegerField(_('Уровень сложности'), null=True, blank=True)
    comfort_level = models.PositiveIntegerField(_('Уровень комфорта'), null=True, blank=True)
    tour_excluded_services = models.JSONField(_("Не включенные услуги"), null=True, blank=True)
    tour_included_services = models.JSONField(_("Включенные услуги"), null=True, blank=True)
    languages = models.JSONField(_("Языки"), null=True, blank=True)
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    duration = models.PositiveIntegerField(_("Продолжительность тура в днях"), null=True, blank=True)
    phone = PhoneNumberField(_('Номер телефона'), null=True, blank=True)
    email = models.EmailField(_('email'), null=True, blank=True)

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        ordering = ['id']


class Traveler(models.Model):
    last_name = models.CharField(_('Фамилия'), max_length=50, null=True, blank=True)   
    middle_name = models.CharField(_('Отчество'), max_length=50, null=True, blank=True)   
    first_name = models.CharField(_('Имя'), max_length=50, null=True, blank=True)
    birth_date = models.DateField(_('Дата рождения'), null=True, blank=True)
    index_number = models.PositiveIntegerField(_('Порядковый номер'), null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='travelers', verbose_name=_('Заказ'))

    class Meta:
        verbose_name = _('Путешественник')
        verbose_name_plural = _('Путешественники')
        ordering = ['id']

