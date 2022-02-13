from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from unidecode import unidecode
import os

# Create your models here.
def geo_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'geoplaces/{0}/{1}{2}'.format(slugify(unidecode(instance.name)), slugify(unidecode(name)), extension)


class Region(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    image = models.ImageField(_("Фото"), upload_to=geo_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')

class Country(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='countries', verbose_name=_('Регион'),)
    image = models.ImageField(_("Фото"), upload_to=geo_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Страна')
        verbose_name_plural = _('Страны')

class City(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='cities', verbose_name=_('Страна'), null=True, blank=True)
    russian_region = models.ForeignKey('RussianRegion', on_delete=models.CASCADE, related_name='cities', verbose_name=_('Страна'), null=True, blank=True)
    image = models.ImageField(_("Фото"), upload_to=geo_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')

class RussianRegion(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    image = models.ImageField(_("Фото"), upload_to=geo_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Регион России')
        verbose_name_plural = _('Регионы России')