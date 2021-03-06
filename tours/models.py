from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import default, slugify
from unidecode import unidecode
import os
from datetime import timedelta, datetime
from django.db.models.query import Prefetch
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import ArrayField
from ckeditor.fields import RichTextField
from geoplaces.models import Destination
from utils.images import get_tmb_path


def get_booking_delay():
    return timedelta(days=3)

def get_mtm_tour_basic(obj):
    return obj.tours.first().tour_basic.id


def tour_image_path(instance, filename):
    name, extension = os.path.splitext(filename)
    class_name = instance.__class__.__name__
    if class_name == 'TourWallpaper':
        folder = f'expert/{instance.tour_basic.expert.id}/tour/{instance.tour_basic.id}/wallpapers'
    elif class_name == 'TourDayImage':
        folder = f'expert/{instance.tour_basic.expert.id}/tour/{instance.tour_basic.id}/days'
    elif class_name == 'TourPropertyImage':
        folder = f'expert/{instance.tour_basic.expert.id}/tour/{instance.tour_basic.id}/properties'
    elif class_name == 'TourImage':
        folder = f'expert/{instance.tour_basic.expert.id}/tour/{instance.tour_basic.id}/gallary'
    elif class_name == 'TourPlanImage':
        folder = f'expert/{instance.tour_basic.expert.id}/tour/{instance.tour_basic.id}/plans'
    elif class_name == 'TourGuestGuideImage':
        folder = f'expert/{instance.expert.id}/guestguide'
    else:
        folder = f'{slugify(unidecode(instance.__class__.__name__))}'
    return '{0}/{1}{2}'.format(folder, slugify(unidecode(name)), extension)

def tour_types_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'tourtypes/{0}/{1}{2}'.format(slugify(unidecode(instance.name)), slugify(unidecode(name)), extension)


class TourType(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    slug = models.SlugField(max_length = 255, null=True, blank=True)
    image = models.ImageField(_("Фото"), upload_to=tour_types_path, max_length=255, null=True, blank=True)
    alt =  models.CharField(_('alt текст'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Тип тура')
        verbose_name_plural = _('Типы туров')
    
    @property
    def tmb_image(self):
        return get_tmb_path(self.image.url) if self.image else None


class TourBasic(models.Model):
    expert = models.ForeignKey("accounts.Expert", verbose_name=_('Эксперт'), on_delete=models.CASCADE, related_name='tours')
    reviews_count = models.IntegerField(_('Кол-во отзывов'), default=0)
    rating = models.DecimalField(_('Рейтинг'), decimal_places=1, max_digits=2, default=0)
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Основа тура')
        verbose_name_plural = _('Основы туров')


class TourPropertyType(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Тип размещения')
        verbose_name_plural = _('Типы размещения')


class TourAccomodation(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Размещения')
        verbose_name_plural = _('Размещение')

class TourPropertyImage(models.Model):
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255)
    expert = models.ForeignKey('accounts.Expert', on_delete=models.CASCADE, related_name='tour_property_images', null=True, blank=True)
    tour_basic = models.ForeignKey("TourBasic", verbose_name=_('Основа тура'), on_delete=models.CASCADE, related_name='tour_property_images', null=True, blank=True)
    
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
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255, null=True, blank=True)
    expert = models.ForeignKey('accounts.Expert', on_delete=models.CASCADE, related_name='tour_images', null=True, blank=True)
    tour_basic = models.ForeignKey("TourBasic", verbose_name=_('Основа тура'), on_delete=models.CASCADE, related_name='tour_images', null=True, blank=True)
    
    class Meta:
        verbose_name = _('Фото тура')
        verbose_name_plural = _('Фотографии туров')
        ordering =  ['-id']
    
    @property
    def tmb_image(self):
        if self.image:
            tmb_path = get_tmb_path(self.image.url)
            return tmb_path
        return None


class TourDayImage(models.Model):
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255, null=True, blank=True)
    expert = models.ForeignKey('accounts.Expert', on_delete=models.CASCADE, related_name='tour_day_images', null=True, blank=True)
    tour_basic = models.ForeignKey("TourBasic", verbose_name=_('Основа тура'), on_delete=models.CASCADE, related_name='tour_day_images', null=True, blank=True)

    class Meta:
        verbose_name = _('Фото дня тура')
        verbose_name_plural = _('Фотографии дней туров')
    
    @property
    def tmb_image(self):
        if self.image:
            tmb_path = get_tmb_path(self.image.url)
            return tmb_path
        return None


class TourPlanImage(models.Model):
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255, null=True, blank=True)
    expert = models.ForeignKey('accounts.Expert', on_delete=models.CASCADE, related_name='tour_plan_images', null=True, blank=True)
    tour_basic = models.ForeignKey("TourBasic", verbose_name=_('Основа тура'), on_delete=models.CASCADE, related_name='tour_plan_images', null=True, blank=True)

    @property
    def tmb_image(self):
        return get_tmb_path(self.image.url) if self.image else None
    
    class Meta:
        verbose_name = _('Фото чем займемся')
        verbose_name_plural = _('Фотографии чем займемся')
        ordering = ['id']


class TourGuestGuideImage(models.Model):
    image = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255, null=True, blank=True)
    expert = models.ForeignKey('accounts.Expert', on_delete=models.CASCADE, related_name='tour_guest_guide_images', null=True, blank=True)

    @property
    def tmb_image(self):
        return get_tmb_path(self.image.url) if self.image else None
    
    class Meta:
        verbose_name = _('Фото приглашенного гида')
        verbose_name_plural = _('Фотографии приглашенных гидов')
        ordering = ['id']


class TourWallpaper(models.Model):
    wallpaper = models.ImageField(_('Фото'), upload_to=tour_image_path, max_length=255, null=True, blank=True)
    expert = models.ForeignKey('accounts.Expert', on_delete=models.CASCADE, related_name='tour_wallpapers', null=True, blank=True)
    tour_basic = models.ForeignKey("TourBasic", verbose_name=_('Основа тура'), on_delete=models.CASCADE, related_name='tour_wallpapers', null=True, blank=True)

    @property
    def tmb_wallpaper(self):
        return get_tmb_path(self.wallpaper.url) if self.wallpaper else None
    
    class Meta:
        verbose_name = _('Обложка тура')
        verbose_name_plural = _('Обложки тура')
        ordering = ['id']

class ImportantTitle(models.Model):
    title = models.CharField(_('Заголовок'), max_length=150, null=True, blank=True)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Важно знать')
        verbose_name_plural = _('Важно знать')
        ordering = ['id']


class Important(models.Model):
    title = models.CharField(_('Заголовок'), max_length=150, null=True, blank=True)
    body = models.TextField(_('Текст'), null=True, blank=True)
    required = models.BooleanField(default=False)
    tour = models.ForeignKey("Tour", on_delete=models.CASCADE, related_name='important_to_know', null=True, blank=True )

    class Meta:
        ordering = ['id']



class TourManager(models.Manager):
    pass


class TourQuerySet(models.QuerySet):
    def actives(self):
        return self.filter(is_active=True)
    
    def prefetched(self):
        tour_basic = TourBasic.objects.prefetch_related('expert')
        prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
        start_destination = Destination.objects.prefetch_related('region')
        prefetch_start_destination = Prefetch('start_destination', start_destination)
        return self.prefetch_related(prefetch_tour_basic, prefetch_start_destination, 'start_city', 'start_region', 'finish_destination', 'finish_city', 'finish_region', 'basic_type', 'additional_types', 'tour_property_types', 'tour_property_images', 'tour_images', 'languages', 'currency', 'prepay_currency', 'accomodation',)
    
    def in_sale(self): 
        return self.filter(is_active=True).filter(direct_link=False).filter(models.Q(booking_delay__lte=models.F('start_date') - datetime.today().date() - models.F('postpay_days_before_start')))
    
    def with_discounted_price(self):
        return self.annotate(
                discounted_price = models.Case(
                    models.When(models.Q(discount__isnull=True) or models.Q(discount=0), then=models.F('price')),
                    models.When(~models.Q(discount__isnull=True) and ~models.Q(discount_starts__isnull=True) and models.Q(discount__gt=0) and models.Q(discount_starts__gte=datetime.today()) and models.Q(discount_finish__gte=datetime.today()) and models.Q(discount_in_prc=True), then=models.F('price') - models.F('price')*models.F('discount')/100),
                    models.When(~models.Q(discount__isnull=True) and models.Q(discount__gt=0) and models.Q(discount_starts__lte=datetime.today()) and models.Q(discount_finish__gte=datetime.today()) and models.Q(discount_in_prc=False), then=models.F('price') - models.F('discount')),
                )
            )

class Tour(models.Model):
    tour_basic = models.ForeignKey("TourBasic", verbose_name=_('Основа тура'), on_delete=models.CASCADE, related_name='tours', null=True, blank=True)
    name = models.CharField(_('Название'), max_length=180, null=True, blank=True)
    slug = models.SlugField(max_length = 255, null=True, blank=True)
    is_draft = models.BooleanField(_('Черновик'), default=True)
    is_active = models.BooleanField(default=False)
    on_moderation = models.BooleanField(_('На модерации'), default=False)
    wallpaper = models.ForeignKey("TourWallpaper", verbose_name=_('Главное фото'), on_delete=models.CASCADE, related_name='tour', null=True, blank=True)
    basic_type = models.ForeignKey("TourType", verbose_name=_("Основной тип тура"), on_delete=models.CASCADE, related_name='tours_by_basic_type', null=True, blank=True)
    additional_types = models.ManyToManyField("TourType", verbose_name=_("Дополнительные типы тура"), related_name='tours_by_additional_types', blank=True)
    start_region = models.ForeignKey("geoplaces.Region", verbose_name=_("Регион начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_region', null=True, blank=True)
    finish_region = models.ForeignKey("geoplaces.Region", verbose_name=_("Регион завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_region', null=True, blank=True)
    start_destination = models.ForeignKey("geoplaces.Destination", verbose_name=_("Направление начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_destination', null=True, blank=True)
    finish_destination = models.ForeignKey("geoplaces.Destination", verbose_name=_("Направление завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_destination', null=True, blank=True)
    start_city = models.ForeignKey("geoplaces.City", verbose_name=_("Город начала путешествия"), on_delete=models.CASCADE, related_name='tours_by_start_city', null=True, blank=True)
    finish_city = models.ForeignKey("geoplaces.City", verbose_name=_("Город завершения путешествия"), on_delete=models.CASCADE, related_name='tours_by_finish_city', null=True, blank=True)
    week_recurrent = models.BooleanField(_('Повторять еженедельно'), default=False)
    month_recurrent = models.BooleanField(_('Повторять ежемесячно'), default=False)
    description = RichTextField(_('Описание тура'), null=True, blank=True)
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
    instant_booking = models.BooleanField(_('Моментальное бронирование'), default=False)
    members_number = models.PositiveIntegerField(_('Колличество мест'), default=0)
    vacants_number = models.PositiveIntegerField(_('Колличество свободных мест'), default=0)
    price_comment = models.CharField(_('Коментарий к стоимости'), max_length=255, null=True, blank=True)
    prepay_amount = models.PositiveIntegerField(_('Размер предоплаты'), default=15)
    prepay_in_prc = models.BooleanField(_('Предоплата в процентах'), default=True)
    prepay_currency = models.ForeignKey('currencies.Currency', verbose_name=_("Валюта предоплаты"), on_delete=models.CASCADE, related_name='tours_by_prepay_currency', null=True, blank=True)
    postpay_on_start_day = models.BooleanField(_('Постоплата в день старта'), default=False)
    postpay_days_before_start = models.DurationField(_('Дни внесения полной суммы до старта'), default=timedelta(days=5), blank=True, null=True,)
    team_member = models.ForeignKey('accounts.TeamMember', verbose_name=_("Гид"), on_delete=models.CASCADE, related_name='tours', null=True, blank=True)
    currency = models.ForeignKey('currencies.Currency', verbose_name=_("Валюта"), on_delete=models.CASCADE, related_name='tours', null=True, blank=True)
    cost = models.IntegerField(_('Стоимость со скидкой'), null=True, blank=True)
    price = models.IntegerField(_('Цена'), null=True, blank=True)
    discount_starts = models.DateField(_('Действует с'), null=True, blank=True)
    discount_finish = models.DateField(_('Действует до'), null=True, blank=True)
    discount_in_prc = models.BooleanField(_('Скидка в процентах'), default=True)
    discount = models.IntegerField(_('Скидка'), null=True, blank=True)
    languages = models.ManyToManyField('languages.Language', verbose_name=_('Языки тура'), related_name='tours', blank=True)
    is_guaranteed = models.BooleanField(_('Тур гарантирован'), default=False, null=True, blank=True)
    flight_included = models.BooleanField(_('Перелет включен'), default=False, null=True, blank=True)
    scouting = models.BooleanField(_('Разведка'), default=False, null=True, blank=True)
    age_starts = models.PositiveIntegerField(_('Мин возраст участника тура'), default=15, null=True, blank=True)
    age_ends = models.PositiveIntegerField(_('Макс возраст участника тура'), default=85, null=True, blank=True)
    media_link = models.URLField(_('Ссылка на видео тура'), max_length=255, null=True, blank=True)
    air_tickets = models.TextField(_('Авиабилеты'), null=True, blank=True)
    views_count = models.PositiveIntegerField(_('Просмотры'), null=True, blank=True, default=0)
    sold = models.PositiveIntegerField(_('Продажи'), null=True, blank=True)
    tour_property_types = models.ManyToManyField('TourPropertyType', related_name='tours', verbose_name=_("Типы размещения"), blank=True)
    accomodation = models.ManyToManyField('TourAccomodation', related_name='tours', verbose_name=_("Размещения"), blank=True)
    tour_addetional_services = models.JSONField(_("Дополнительные услуги"), blank=True,  null=True)
    tour_excluded_services = models.JSONField(_("Не включенные услуги"),  null=True, blank=True)
    tour_included_services = models.JSONField(_("Включенные услуги"), null=True, blank=True)
    main_impressions = models.JSONField(_("Главные впечатления"), null=True, blank=True)
    plan = models.JSONField(_("Чем займемся"), null=True, blank=True)
    tour_days = models.JSONField(_("Дни тура"), blank=True, null=True)
    tour_images = models.ManyToManyField('TourImage', related_name='tours', verbose_name=_("Галерея тура"), blank=True)
    tour_property_images = models.ManyToManyField('TourPropertyImage', related_name='tours', verbose_name=_("Фото размещений"), blank=True)
    guest_guide = models.JSONField(_("Приглашенный гид"), null=True, blank=True)
    guest_requirements = RichTextField(_('Требования к гостю'), null=True, blank=True)
    take_with = RichTextField(_('Что взять с собой'), null=True, blank=True)
    key_features = RichTextField(_('Ключевые особенности'), null=True, blank=True)
    new_to_see = RichTextField(_('Что нового я увижу'), null=True, blank=True)
    completed_sections = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)
    booking_delay = models.DurationField(default=get_booking_delay)
    direct_link = models.BooleanField(_('Доступ по прямой ссылке'), default=False)
    map = models.JSONField(_('Карта'), null=True, blank=True)
   
    objects = TourManager.from_queryset(TourQuerySet)()

    class Meta:
        verbose_name = _('Тур')
        verbose_name_plural = _('Туры')
    
    def __str__(self):
        return self.name if self.name else 'безымянный тур'
    
class ModeratedTour(Tour):
    class Meta:
        verbose_name = _('Тур на модерации')
        verbose_name_plural = _('Туры на модерации')
        proxy = True


class DeclineReason(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(_('Причина отказа'))
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='decline_reasons')
    staff = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='decline_reasons')

