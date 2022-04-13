from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Currency(models.Model):
    short_name = models.CharField(_('Краткое название'), max_length=7)
    name = models.CharField(_('Название'), max_length=50)
    rate = models.DecimalField(_('Курс'), max_digits=12, decimal_places=2, default=1)
    sign = models.CharField(_('Знак'), max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Валюта')
        verbose_name_plural = _('Валюты')