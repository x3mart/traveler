from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
def get_order_id():
    pass

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', _('Ожидает оплаты')
        PREPAYMENT = 'prepayment', _('Предоплата')
        FULLPREPAYMENT = 'fullprepayment', _('Оплачено')
        FULLPAYMENT = 'fullpayment', _('Закрыт')
        
    customer = models.ForeignKey('accounts.Customer', on_delete=models.PROTECT, related_name='customers_orders', verbose_name=_('Путешествиник'))
    expert = models.ForeignKey('accounts.Expert', on_delete=models.PROTECT, related_name='experts_orders', verbose_name=_('Эксперт'))
    tour =  models.ForeignKey('tours.TourAdvanced', on_delete=models.PROTECT, related_name='tours_orders', verbose_name=_('Тур'))
    tour_name = models.CharField(_('Название тура'), max_length=255)
    tour_start_date = models.DateField(_('Дата начала'))
    tour_finish_date = models.DateField(_('Дата завершения'))
    tour_price = models.PositiveIntegerField(_('Цена'))
    members_number = models.PositiveIntegerField(_('Количево участников'))
    cost = models.PositiveIntegerField(_('Стоимость тура'))
    status = models.CharField(_('Статус'), max_length=15)


    