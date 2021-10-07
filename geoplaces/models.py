from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Region(models.Model):
    name = models.CharField(_('Название'), max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')

class Country(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='countries', verbose_name=_('Регион'),)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Страна')
        verbose_name_plural = _('Страны')

class City(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='cities', verbose_name=_('Страна'))


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')