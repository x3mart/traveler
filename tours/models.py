from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import default, slugify
from unidecode import unidecode
import os
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from utils.images import get_tmb_path


def tour_image_path(instance, filename):
    name, extension = os.path.splitext(filename)
    class_name = instance.__class__.__name__
    if class_name == 'Tour':
        folder = f'{slugify(unidecode(instance.name))}/wallpaper'
    elif class_name == 'TourDay':
        folder = f'{slugify(unidecode(instance.tour.name))}/day-{instance.number}'
    elif class_name == 'TourPropertyImage':
        folder = f'{slugify(unidecode(instance.tour.name))}'
    elif class_name == 'TourImage':
        folder = f'{slugify(unidecode(instance.tour.name))}/gallary'
    else:
        folder = f'{slugify(unidecode(instance.tour.name))}/{slugify(unidecode(instance.__class__.__name__))}/{slugify(unidecode(instance.name))}'
    return 'tours/{0}/{1}{2}'.format(folder, slugify(unidecode(name)), extension)

def tour_types_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'tourtypes/{0}/{1}{2}'.format(slugify(unidecode(instance.name)), slugify(unidecode(name)), extension)


class TourType(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    image = models.ImageField(_("Фото"), upload_to=tour_types_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Тип тура')
        verbose_name_plural = _('Типы туров')



class Tour(models.Model):
    expert = models.ForeignKey("accounts.Expert", verbose_name=_('Эксперт'), on_delete=models.CASCADE, related_name='tours')
    is_draft = models.BooleanField(_('Черновик'), default=True)
    is_active = models.BooleanField(default=False)
    on_moderation = models.BooleanField(_('На модерации'), default=False)
    rating = models.DecimalField(_('Рейтинг'), decimal_places=1, max_digits=2, null=True, blank=True)
    reviews_count = models.IntegerField(_('Кол-во отзывов'), default=0)
    name = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    wallpaper = models.ImageField(_('Главное фото'), max_length=255, upload_to=tour_image_path, null=True, blank=True)
    basic_type = models.ForeignKey("TourType", verbose_name=_("Основной тип тура"), on_delete=models.CASCADE, related_name='tours_by_basic_type', null=True, blank=True)
    additional_types = models.ManyToManyField("TourType", verbose_name=_("Дополнительные типы тура"), related_name='tours_by_additional_types', blank=True)
    start_region = models.ForeignKey("geoplaces.Region", verbose_name=_("Регион начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_region', null=True, blank=True)
    finish_region = models.ForeignKey("geoplaces.Region", verbose_name=_("Регион завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_region', null=True, blank=True)
    start_country = models.ForeignKey("geoplaces.Country", verbose_name=_("Страна начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_country', null=True, blank=True)
    finish_country = models.ForeignKey("geoplaces.Country", verbose_name=_("Страна завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_country', null=True, blank=True)
    start_russian_region = models.ForeignKey("geoplaces.RussianRegion", verbose_name=_("Российский регион начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_russian_region', null=True, blank=True)
    finish_russian_region = models.ForeignKey("geoplaces.RussianRegion", verbose_name=_("Российский регион завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_russian_region', null=True, blank=True)
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
    hotel_name = models.CharField(_('Наименование отеля'), max_length=255, null=True, blank=True) 
    start_date = models.DateField(_('Дата начала'), null=True, blank=True)
    duration = models.PositiveIntegerField(_("Продолжительность тура в днях"), null=True, blank=True)
    finish_date = models.DateField(_('Дата завершения'), null=True, blank=True)
    start_time = models.TimeField(_('Время старта'), null=True, blank=True)
    finish_time = models.TimeField(_('Время завершения'), null=True, blank=True)
    direct_link = models.BooleanField(_('Доступ по прямой ссылке'), default=False)
    instant_booking = models.BooleanField(_('Моментальное бронирование'), default=False)
    members_number = models.PositiveIntegerField(_('Колличество мест'), default=0)
    vacants_number = models.PositiveIntegerField(_('Колличество свободных мест'), default=0)
    price_comment = models.CharField(_('Коментарий к стоимости'), max_length=255, null=True, blank=True)
    prepay_amount = models.PositiveIntegerField(_('Размер предоплаты'), default=15)
    prepay_in_prc = models.BooleanField(_('Предоплата в процентах'), default=True)
    prepay_currency = models.ForeignKey('currencies.Currency', verbose_name=_("Валюта предоплаты"), on_delete=models.CASCADE, related_name='tours_by_prepay_currency', null=True, blank=True)
    prepay_starts = models.DateField(_('Действует с'), null=True, blank=True)
    prepay_finish = models.DateField(_('Действует до'), null=True, blank=True)
    postpay_on_start_day = models.BooleanField(_('Постоплата в день старта'), default=False)
    postpay_days_before_start = models.PositiveIntegerField(_('Дни внесения полной суммы до старта'), null=True, blank=True)
    team_member = models.ForeignKey('accounts.TeamMember', verbose_name=_("Гид"), on_delete=models.CASCADE, related_name='tours', null=True, blank=True)
    currency = models.ForeignKey('currencies.Currency', verbose_name=_("Валюта"), on_delete=models.CASCADE, related_name='tours', null=True, blank=True)
    cost = models.IntegerField(_('Стоимость со скидкой'), null=True, blank=True)
    price = models.IntegerField(_('Цена'), null=True, blank=True)
    discount = models.IntegerField(_('Скидка'), null=True, blank=True)
    languages = models.ManyToManyField('languages.Language', verbose_name=_('Языки тура'), related_name='tours', blank=True)
    is_guaranteed = models.BooleanField(_('Тур гарантирован'), default=False, null=True, blank=True)
    flight_included = models.BooleanField(_('Перелет включен'), default=False, null=True, blank=True)
    scouting = models.BooleanField(_('Разведка'), default=False, null=True, blank=True)
    age_starts = models.PositiveIntegerField(_('Мин возраст участника тура'), default=15, null=True, blank=True)
    age_ends = models.PositiveIntegerField(_('Мин возраст участника тура'), default=85, null=True, blank=True)
    media_link = models.URLField(_('Ссылка на видео тура'), max_length=150, null=True, blank=True)
    accomodation = models.CharField(_('РАЗМЕЩЕНИЕ'), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Тур основа')
        verbose_name_plural = _('Туры основа')
    
    def __str__(self):
        return self.name
   
    @property
    def tmb_wallpaper(self):
        if self.wallpaper:
            tmb_path = get_tmb_path(self.wallpaper.url)
            return tmb_path
        return None

class TourPropertyType(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    tours = models.ManyToManyField('Tour', related_name='tour_property_types')

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
    tour = models.ForeignKey("Tour", verbose_name=_("Тур"), on_delete=models.CASCADE, related_name='tour_property_images')

    
    class Meta:
        verbose_name = _('Фото размещения')
        verbose_name_plural = _('Фотографии размещений')
    
    @property
    def tmb_image(self):
        if self.image:
            tmb_path = get_tmb_path(self.image.url)
            return tmb_path
        return None


class TourImage(models.Model):
    name = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Описание'), null=True, blank=True)
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    tour = models.ForeignKey("Tour", verbose_name=_("Тур"), on_delete=models.CASCADE, related_name='tour_images', max_length=255, null=True, blank=True)
    
    class Meta:
        verbose_name = _('Фото тура')
        verbose_name_plural = _('Фотографии туров')
        ordering =  ['tour', '-id']
    
    @property
    def tmb_image(self):
        if self.image:
            tmb_path = get_tmb_path(self.image.url)
            return tmb_path
        return None


class TourDay(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    location =  models.CharField(_('Локация'), max_length=255, null=True, blank=True)
    description = RichTextField(_('Описание'))
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='tour_days', verbose_name=_('Тур'))

    def __str__(self):
        return self.tour.name
    
    class Meta:
        verbose_name = _('День тура')
        verbose_name_plural = _('Дни туров')
        ordering = ['id']


class TourDayImage(models.Model):
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)
    tour_day = models.ForeignKey("TourDay", verbose_name=_("День тура"), on_delete=models.CASCADE, max_length=255, null=True, blank=True, related_name='tour_day_images')

    class Meta:
        verbose_name = _('Фото дня тура')
        verbose_name_plural = _('Фото дней туров')
    
    @property
    def tmb_image(self):
        if self.image:
            tmb_path = get_tmb_path(self.image.url)
            return tmb_path
        return None


class TourImpression(models.Model):
    name = models.CharField(_('Название'), max_length=150)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='main_impressions', verbose_name=_('Тур'))

    class Meta:
        verbose_name = _('Главное впечатление')
        verbose_name_plural = _('Главные впечатления')


class TourIncludedService(models.Model):
    name = models.CharField(_('Название'), max_length=150)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='tour_included_services', verbose_name=_('Тур'))

    class Meta:
        verbose_name = _('Входит в стоимость')
        verbose_name_plural = _('Входит в стоимость')


class TourExcludedService(models.Model):
    name = models.CharField(_('Название'), max_length=150)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='tour_excluded_services', verbose_name=_('Тур'))

    class Meta:
        verbose_name = _('Не входит в стоимость')
        verbose_name_plural = _('Не входит в стоимость')


class TourAddetionalService(models.Model):
    name = models.CharField(_('Название'), max_length=150)
    description = RichTextField(_('Описание'))
    currency = models.ForeignKey('currencies.Currency', verbose_name=_("Валюта"), on_delete=models.CASCADE, related_name='tour_addetional_service', null=True, blank=True)
    price = models.IntegerField(_('Цена'), null=True, blank=True)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='tour_addetional_services', verbose_name=_('Тур'))

    class Meta:
        verbose_name = _('Дополнительная услуга')
        verbose_name_plural = _('Дополнительнае услуги')