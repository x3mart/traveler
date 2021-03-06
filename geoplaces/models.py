from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from unidecode import unidecode
import os
from utils.images import get_tmb_path
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField

# Create your models here.
def geo_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'geoplaces/{0}/{1}{2}'.format(slugify(unidecode(instance.name)), slugify(unidecode(name)), extension)


class Region(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    slug = models.SlugField(max_length = 255, null=True, blank=True)
    image = models.ImageField(_("Фото"), upload_to=geo_path, max_length=255, null=True, blank=True)
    map_icon = models.FileField(_("Изображение карты"), upload_to=geo_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Регион Мира')
        verbose_name_plural = _('Регионы Мира')
    
    @property
    def tmb_image(self):
        return get_tmb_path(self.image.url) if self.image else None

class Destination(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    slug = models.SlugField(max_length = 255, null=True, blank=True)
    # counry_code = models.CharField(_('Краткое название'), null=True, blank=True, max_length=20)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='destinations', verbose_name=_('Регион Мира'), null=True, blank=True)
    image = models.ImageField(_("Фото"), upload_to=geo_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    views_count = models.PositiveIntegerField(_('Просмотры'), null=True, blank=True, default=0)

    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = _('Тур направление')
        verbose_name_plural = _('Тур направления')
    
    @property
    def tmb_image(self):
        return get_tmb_path(self.image.url) if self.image else None

class Country(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    slug = models.SlugField(max_length = 255, null=True, blank=True)
    counry_code = models.CharField(_('Краткое название'), null=True, blank=True, max_length=20)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='countries', verbose_name=_('Регион Мира'), null=True, blank=True)
    image = models.ImageField(_("Фото"), upload_to=geo_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = _('Страна')
        verbose_name_plural = _('Страны')
    
    @property
    def tmb_image(self):
        return get_tmb_path(self.image.url) if self.image else None

class City(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    slug = models.SlugField(max_length = 255, null=True, blank=True)
    foreign_id = models.IntegerField(_('Сторонний ключ'), null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='cities', verbose_name=_('Страна'), null=True, blank=True)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE, related_name='cities', verbose_name=_('Страна'), null=True, blank=True)
    image = models.ImageField(_("Фото"), upload_to=geo_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
    
    @property
    def tmb_image(self):
        return get_tmb_path(self.image.url) if self.image else None
