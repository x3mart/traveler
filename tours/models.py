from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from unidecode import unidecode
import os


def property_image_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'property/{0}/{1}{2}'.format(slugify(unidecode(instance.tour.name)), slugify(unidecode(name)), extension)


class TourType(models.Model):
    name = models.CharField(_('Название'), max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Тип тура')
        verbose_name_plural = _('Типы туров')


class Tour(models.Model):
    pass


class TourImage(models.Model):
    pass


class PropertyType(models.Model):
    name = models.CharField(_('Название'), max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Тип размещения')
        verbose_name_plural = _('Типы размещения')


class PropertyImage(models.Model):
    name = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Название'), null=True, blank=True)
    image = models.ImageField(_('Фото'), upload_to=property_image_path, max_length=255)
    tour = models.ForeignKey("Tour", verbose_name=_("Тур"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _('Тип размещения')
        verbose_name_plural = _('Типы размещения')


class TourDay(models.Model):
    number = models.PositiveIntegerField(_('Номер'))
    name = models.CharField(_('Название'), max_length=255)
    location =  models.CharField(_('Локация'), max_length=255, null=True, blank=True)
    description =  models.CharField(_('Описание'), max_length=255)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='tour_days')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('День тура')
        verbose_name_plural = _('Дни туров')
        ordering = ['number', 'tour']


class TourDayImage(models.Model):
    pass