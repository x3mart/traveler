from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from unidecode import unidecode
import os
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField

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
        verbose_name = _('Регион Мира')
        verbose_name_plural = _('Регионы Мира')

class Country(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    foreign_id = models.IntegerField(_('Сторонний ключ'), null=True, blank=True)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='countries', verbose_name=_('Регион Мира'), null=True, blank=True)
    image = models.ImageField(_("Фото"), upload_to=geo_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Страна')
        verbose_name_plural = _('Страны')

class City(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    foreign_id = models.IntegerField(_('Сторонний ключ'), null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='cities', verbose_name=_('Страна'), null=True, blank=True)
    country_region = models.ForeignKey('CountryRegion', on_delete=models.CASCADE, related_name='cities', verbose_name=_('Регион Страны'), null=True, blank=True)
    image = models.ImageField(_("Фото"), upload_to=geo_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    search_vector = models.CharField(null=True, editable=False, max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            GinIndex(fields=['name'], name='search_vector_idx', opclasses=['gin_trgm_ops'])
        ]
        verbose_name = _('Город')
        verbose_name_plural = _('Города')

class CountryRegion(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    foreign_id = models.IntegerField(_('Сторонний ключ'), null=True, blank=True)
    image = models.ImageField(_("Фото"), upload_to=geo_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='country_regions', verbose_name=_('Страна'), null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Регион Страны')
        verbose_name_plural = _('Регионы Страны')


class VKCity(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    foreign_id = models.IntegerField(_('Сторонний ключ'), null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='vkcities', verbose_name=_('Страна'), null=True, blank=True)
    country_region = models.ForeignKey('CountryRegion', on_delete=models.CASCADE, related_name='vkcities', verbose_name=_('Регион Страны'), null=True, blank=True)