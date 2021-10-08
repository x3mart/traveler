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


class TourBasic(models.Model):
    expert = models.ForeignKey("accounts.Expert", verbose_name=_("Основной тип"), on_delete=models.CASCADE, related_name='tours')
    is_draft = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    moderation = models.BooleanField(default=False)
    name = models.CharField(_('Название'), max_length=255)
    basic_type = models.ForeignKey("TourType", verbose_name=_("Основной тип"), on_delete=models.CASCADE, related_name='tours_by_basic_type', null=True, blank=True)
    additional_types = models.ManyToManyField("TourType", verbose_name=_("Основной тип"), related_name='tours_by_additional_types')
    start_region =  models.ForeignKey("geoplaces.Region", verbose_name=_("Регион начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_region', null=True, blank=True)
    finish_region =  models.ForeignKey("geoplaces.Region", verbose_name=_("Регион завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_region', null=True, blank=True)
    start_country =  models.ForeignKey("geoplaces.Country", verbose_name=_("Страна начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_country', null=True, blank=True)
    finish_country =  models.ForeignKey("geoplaces.Country", verbose_name=_("Страна завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_country', null=True, blank=True)
    start_city = models.ForeignKey("geoplaces.City", verbose_name=_("Город начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_city', null=True, blank=True)
    finish_city = models.ForeignKey("geoplaces.City", verbose_name=_("Город завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_city', null=True, blank=True)
    direct_link = models.BooleanField(_('Доступ по прямой ссылке'), default=False)

    class Meta:
        verbose_name = _('Тур')
        verbose_name_plural = _('Туры')


class TourAdvanced(models.Model):
    start_time = models.TimeField(_('Время прибытия'), null=True, blank=True)
    finish_time = models.TimeField(_('Время завершения'), null=True, blank=True)
    instant_booking = models.BooleanField(_('Моментальное бронирование'), default=False)
    members_number = models.PositiveIntegerField(_('Колличество мест'))
    prepayment = models.PositiveIntegerField(_('Предоплата в %'), default=15)
    postpayment = models.PositiveIntegerField(_('Дни внесения полной суммы до старта'), null=True, blank=True)
    week_recurrent = models.BooleanField(_('Повторять еженедельно'), default=False)
    month_recurrent = models.BooleanField(_('Повторять ежемесячно'), default=False)


class PropertyType(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    tours = models.ManyToManyField('TourBasic', related_name='property_types')

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
    tour = models.ForeignKey("TourBasic", verbose_name=_("Тур"), on_delete=models.CASCADE, related_name='property_images')

    
    class Meta:
        verbose_name = _('Тип размещения')
        verbose_name_plural = _('Типы размещения')


class TourImage(models.Model):
    name = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Описание'), null=True, blank=True)
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    tour = models.ForeignKey("TourBasic", verbose_name=_("Тур"), on_delete=models.CASCADE, related_name='tour_images', max_length=255, null=True, blank=True)

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
    tour = models.ForeignKey('TourBasic', on_delete=models.CASCADE, related_name='tour_days')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('День тура')
        verbose_name_plural = _('Дни туров')
        ordering = ['number', 'tour']


class TourDayImage(models.Model):
    name = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Описание'), null=True, blank=True)
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    tour_day = models.ForeignKey("TourDay", verbose_name=_("День тура"), on_delete=models.CASCADE, max_length=255, null=True, blank=True)