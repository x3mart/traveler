from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from unidecode import unidecode
import os
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


def tour_image_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'property/{0}/{1}{2}'.format(slugify(unidecode(instance.tour.name)), slugify(unidecode(name)), extension)

def tour_types_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'tourtypespath/{0}/{1}{2}'.format(slugify(unidecode(instance.name)), slugify(unidecode(name)), extension)


class TourType(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    image = models.ImageField(_("Фото"), upload_to=tour_types_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Тип тура')
        verbose_name_plural = _('Типы туров')


class TourBasic(models.Model):
    expert = models.ForeignKey("accounts.Expert", verbose_name=_('Эксперт'), on_delete=models.CASCADE, related_name='tours')
    is_draft = models.BooleanField(_('Черновик'), default=True)
    is_active = models.BooleanField(default=False)
    on_moderation = models.BooleanField(_('На модерации'), default=False)
    name = models.CharField(_('Название'), max_length=255)
    basic_type = models.ForeignKey("TourType", verbose_name=_("Основной тип тура"), on_delete=models.CASCADE, related_name='tours_by_basic_type', null=True, blank=True)
    additional_types = models.ManyToManyField("TourType", verbose_name=_("Дополнительные типы тура"), related_name='tours_by_additional_types', blank=True)
    start_region = models.ForeignKey("geoplaces.Region", verbose_name=_("Регион начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_region', null=True, blank=True)
    finish_region = models.ForeignKey("geoplaces.Region", verbose_name=_("Регион завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_region', null=True, blank=True)
    start_country = models.ForeignKey("geoplaces.Country", verbose_name=_("Страна начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_country', null=True, blank=True)
    finish_country = models.ForeignKey("geoplaces.Country", verbose_name=_("Страна завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_country', null=True, blank=True)
    start_city = models.ForeignKey("geoplaces.City", verbose_name=_("Город начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_city', null=True, blank=True)
    finish_city = models.ForeignKey("geoplaces.City", verbose_name=_("Город завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_city', null=True, blank=True)
    week_recurrent = models.BooleanField(_('Повторять еженедельно'), default=False)
    month_recurrent = models.BooleanField(_('Повторять ежемесячно'), default=False)
    description = RichTextField(_('Описание тура'), null=True, blank=True)
    plan = RichTextUploadingField(_('Чем займемся'), null=True, blank=True)
    cancellation_terms = RichTextField(_('Условия отмены'), null=True, blank=True)
    difficulty_level = models.PositiveIntegerField(_('Уровень сложности'), default=1)
    difficulty_description = RichTextField(_('Описание сложностей'), null=True, blank=True)
    comfort_level = models.PositiveIntegerField(_('Уровень комфорта'), default=3)
    babies_alowed = models.BooleanField(_('Можно с маленькими детьми'), default=False)
    animals_not_exploited = models.BooleanField(_('Животные не эксплуатируются'), default=False)

    class Meta:
        verbose_name = _('Тур основа')
        verbose_name_plural = _('Туры основа')


class TourAdvanced(models.Model):
    basic_tour = models.ForeignKey("TourBasic", verbose_name=_("Тур основа"), on_delete=models.CASCADE, related_name='advanced_tours')
    start_date = models.TimeField(_('Дата начала'), null=True, blank=True)
    finish_date = models.TimeField(_('Дата завершения'), null=True, blank=True)
    start_time = models.TimeField(_('Время старта'), null=True, blank=True)
    finish_time = models.TimeField(_('Время завершения'), null=True, blank=True)
    direct_link = models.BooleanField(_('Доступ по прямой ссылке'), default=False)
    instant_booking = models.BooleanField(_('Моментальное бронирование'), default=False)
    members_number = models.PositiveIntegerField(_('Колличество мест'))
    prepayment = models.PositiveIntegerField(_('Предоплата в %'), default=15)
    postpayment = models.PositiveIntegerField(_('Дни внесения полной суммы до старта'), null=True, blank=True)
    team_member = models.ForeignKey('accounts.TeamMember', verbose_name=_("Гид"), on_delete=models.CASCADE, related_name='advanced_tours', null=True, blank=True)
    currency = models.ForeignKey('currencies.Currency', verbose_name=_("Валюта"), on_delete=models.CASCADE, related_name='advanced_tours', null=True, blank=True)
    cost = models.DecimalField(_('Цена'), max_digits=12, decimal_places=2, null=True, blank=True)
    languages = models.ManyToManyField('languages.Language', verbose_name=_('Языки тура'), related_name='advanced_tours', blank=True)
    is_guaranteed = models.BooleanField(_('Тур гарантирован'), default=False)
    flight_included = models.BooleanField(_('Перелет включен'), default=False)
    scouting = models.BooleanField(_('Разведка'), default=False)
    
    def __str__(self):
        return f'{self.basic_tour.name} {self.start_date} - {self.finish_date}'
    
    class Meta:
        verbose_name = _('Тур доп сведения')
        verbose_name_plural = _('Туры доп сведения')    


class TourPropertyType(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    tours = models.ManyToManyField('TourBasic', related_name='tour_property_types')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Тип размещения')
        verbose_name_plural = _('Типы размещения')


class TourPropertyImage(models.Model):
    name = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Описание'), null=True, blank=True)
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    tour = models.ForeignKey("TourBasic", verbose_name=_("Тур"), on_delete=models.CASCADE, related_name='tour_property_images')

    
    class Meta:
        verbose_name = _('Фото размещения')
        verbose_name_plural = _('Фотографии размещений')


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
    description = RichTextField(_('Описание'))
    tour = models.ForeignKey('TourBasic', on_delete=models.CASCADE, related_name='tour_days', verbose_name=_('Тур'))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('День тура')
        verbose_name_plural = _('Дни туров')
        ordering = ['number', 'tour']
        unique_together = ['number', 'tour']


class TourDayImage(models.Model):
    name = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Описание'), null=True, blank=True)
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    tour_day = models.OneToOneField("TourDay", verbose_name=_("День тура"), on_delete=models.CASCADE, max_length=255, null=True, blank=True, related_name='tour_day_image')

    class Meta:
        verbose_name = _('Фото дня тура')
        verbose_name_plural = _('Фото дней туров')


class TourImpression(models.Model):
    name = models.CharField(_('Название'), max_length=150)
    tour = models.ForeignKey('TourBasic', on_delete=models.CASCADE, related_name='tour_impressions', verbose_name=_('Тур'))

    class Meta:
        verbose_name = _('Главное впечатление')
        verbose_name_plural = _('Главные впечатления')


class TourIncludedService(models.Model):
    name = models.CharField(_('Название'), max_length=150)
    tour = models.ForeignKey('TourBasic', on_delete=models.CASCADE, related_name='tour_included_services', verbose_name=_('Тур'))

    class Meta:
        verbose_name = _('Входит в стоимость')
        verbose_name_plural = _('Входит в стоимость')


class TourExcludedService(models.Model):
    name = models.CharField(_('Название'), max_length=150)
    tour = models.ForeignKey('TourBasic', on_delete=models.CASCADE, related_name='tour_excluded_services', verbose_name=_('Тур'))

    class Meta:
        verbose_name = _('Входит в стоимость')
        verbose_name_plural = _('Входит в стоимость')


class TourAddetionalService(models.Model):
    name = models.CharField(_('Название'), max_length=150)
    description = RichTextField(_('Описание'))
    currency = models.ForeignKey('currencies.Currency', verbose_name=_("Валюта"), on_delete=models.CASCADE, related_name='tour_addetional_service', null=True, blank=True)
    cost = models.DecimalField(_('Цена'), max_digits=12, decimal_places=2, null=True, blank=True)
    tour = models.ForeignKey('TourBasic', on_delete=models.CASCADE, related_name='tour_addetional_services', verbose_name=_('Тур'))

    class Meta:
        verbose_name = _('Дополнительная услуга')
        verbose_name_plural = _('Дополнительнае услуги')