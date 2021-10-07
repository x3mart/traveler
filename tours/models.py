from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from unidecode import unidecode
import os


def tour_image_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'property/{0}/{1}{2}'.format(slugify(unidecode(instance.tour.name)), slugify(unidecode(name)), extension)


class TourType(models.Model):
    name = models.CharField(_('Название'), max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Тип тура')
        verbose_name_plural = _('Типы туров')


class PropertyType(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    tours = models.ManyToManyField('Tour', related_name='property_types')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Тип размещения')
        verbose_name_plural = _('Типы размещения')


class PropertyImage(models.Model):
    name = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Описание'), null=True, blank=True)
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    tour = models.ForeignKey("Tour", verbose_name=_("Тур"), on_delete=models.CASCADE, related_name='property_images')
    
    class Meta:
        verbose_name = _('Тип размещения')
        verbose_name_plural = _('Типы размещения')


class Tour(models.Model):
    is_draft = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    moderation = models.BooleanField(default=False)
    name = models.CharField(_('Название'), max_length=255)
    basic_type = models.ForeignKey("TourType", verbose_name=_("Основной тип"), on_delete=models.CASCADE, related_name='tours_by_basic_type')
    additional_types = models.ManyToManyField("TourType", verbose_name=_("Основной тип"), related_name='tours_by_additional_types')
    region =  models.ForeignKey("geolplaces.Region", verbose_name=_("Регион"), on_delete=models.CASCADE, related_name='tours')
    country =  models.ForeignKey("geolplaces.Country", verbose_name=_("Страна"), on_delete=models.CASCADE, related_name='tours')
    start_city = models.ForeignKey("geolplaces.City", verbose_name=_("Город начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_city')
    finish_city = models.ForeignKey("geolplaces.City", verbose_name=_("Город завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_city')
    start_time = models.TimeField(_('Время прибытия'),)
    finish_time = models.TimeField(_('Время завершения'),)
    direct_link = models.BooleanField(_('Доступ по прямой ссылке'), default=False)
    


class TourImage(models.Model):
    name = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Описание'), null=True, blank=True)
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    tour = models.ForeignKey("Tour", verbose_name=_("Тур"), on_delete=models.CASCADE, related_name='tour_images')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Фото тура')
        verbose_name_plural = _('Фотографии туров')
        ordering =  ['tour', '-id']



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
    name = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Описание'), null=True, blank=True)
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    tour_day = models.ForeignKey("TourDay", verbose_name=_("День тура"), on_delete=models.CASCADE)