from django.db.models import F, Q
from datetime import timedelta, datetime
from django.forms import DurationField
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.db.models.query import Prefetch
from django.db.models import Q, F, Case, Value, When
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError
from django.template.loader import render_to_string
import threading
from django.core.mail import send_mail
from accounts.models import Expert
from currencies.models import Currency
from geoplaces.models import Country, CountryRegion, Region
from geoplaces.serializers import RegionShortSerializer
from orders.paginations import OrderResultsSetPagination
from tours.filters import TourFilter
from tours.mixins import TourMixin
from utils.constants import NOT_MODERATED_FIELDS
from tours.models import DeclineReason, Tour, TourAccomodation, TourBasic, TourDayImage, TourGuestGuideImage, TourImage, TourPlanImage, TourPropertyImage, TourPropertyType, TourType, TourWallpaper
from tours.permissions import TourPermission
from tours.serializers import FilterSerializer, ImageSerializer, TourAccomodationSerializer, TourListSerializer, TourPreviewSerializer, TourPropertyTypeSerializer, TourSerializer, TourTypeSerializer, WallpaperSerializer, TourSetSerializer
from languages.models import Language


class ModerationResultEmailThread(threading.Thread):
    def __init__(self, tour, reason=''):
        self.user = tour.tour_basic.expert
        self.tour = tour
        self.reason = reason
        threading.Thread.__init__(self)
    
    def run(self):
        if self.tour.is_active:
            send_mail('Ваш тур прошел проверку', f'Ваш тур "{self.tour.name}" (старт {self.tour.start_date.strftime("%d-%m-%Y")}) прошел проверку и теперь активен', 'info@traveler.market', [self.user.email,])
        else:
            send_mail('Ваш тур не прошел проверку', f'Ваш тур "{self.tour.name}" (старт {self.tour.start_date.strftime("%d-%m-%Y")}) не прошел проверку по следующей причине: \n \n{self.reason}', 'info@traveler.market', [self.user.email,])


# Create your views here.
class TourViewSet(viewsets.ModelViewSet, TourMixin):
    queryset = Tour.objects.annotate(
                discounted_price = Case(
                    When(Q(discount__isnull=True) or Q(discount=0), then=F('price')),
                    When(~Q(discount__isnull=True) and ~Q(discount_starts__isnull=True) and Q(discount__gt=0) and Q(discount_starts__gte=datetime.today()) and Q(discount_finish__gte=datetime.today()) and Q(discount_in_prc=True), then=F('price') - F('price')*F('discount')/100),
                    When(~Q(discount__isnull=True) and Q(discount__gt=0) and Q(discount_starts__lte=datetime.today()) and Q(discount_finish__gte=datetime.today()) and Q(discount_in_prc=False), then=F('price') - F('discount')),
                )
            ).all()
    serializer_class = TourSerializer
    permission_classes = [TourPermission]
    pagination_class = OrderResultsSetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'id']
    ordering = ['start_date']
    filterset_class = TourFilter

    def get_queryset(self):
        if self.action in ['list',]:
            tour_basic = TourBasic.objects.prefetch_related('expert')
            prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
            qs = super().get_queryset().prefetch_related(prefetch_tour_basic, 'start_country', 'start_city', 'wallpaper', 'currency').only('id', 'name', 'start_date', 'start_country', 'start_city', 'price', 'discount', 'duration', 'tour_basic', 'wallpaper', 'vacants_number', 'currency').filter(is_active=True).filter(direct_link=False).filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start')))
        elif self.action in ['tour_set',]:
            qs = super().get_queryset().prefetch_related('tour_basic', 'start_country', 'currency').only('id', 'name', 'start_date', 'finish_date', 'start_country', 'price', 'cost', 'discount', 'on_moderation', 'is_active', 'is_draft', 'duration', 'sold', 'watched', 'currency', 'tour_basic', 'wallpaper').filter(tour_basic__expert_id=self.request.user.id).order_by('-id')
        else:
            qs = super().get_queryset().prefetch_related('tour_basic', 'start_country', 'start_city', 'start_region', 'start_russian_region', 'finish_russian_region', 'finish_country', 'finish_city', 'finish_region', 'basic_type', 'additional_types', 'tour_property_types', 'tour_property_images', 'tour_images', 'languages', 'currency', 'prepay_currency', 'accomodation',)  
        return qs
    
    def get_serializer_class(self):
        if self.action in ['tour_set',]:
            return TourSetSerializer
        elif self.action in ['preview',]:
            return TourPreviewSerializer
        elif  self.action in ['list',]:
            return TourListSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        data['is_draft'] = True
        tour_basic = TourBasic.objects.create(expert=self.get_expert(request))
        currency = Currency.objects.order_by('id').first()
        tour = Tour.objects.create(currency=currency, tour_basic=tour_basic, **data)
        return Response(TourSerializer(tour).data, status=201)
    
    def update(self, request, *args, **kwargs):
        errors = {}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        instance = self.get_object()
        instance_dict = model_to_dict(instance, exclude=NOT_MODERATED_FIELDS)
        instance = self.set_mtm_fields(request, instance)
        instance = self.set_fk_fields(request, instance)
        instance = self.set_model_fields(data, instance)
        if instance.start_date and instance.finish_date and instance.start_date > instance.finish_date:
            errors['start_date'] = [_("Стартовая дата не может быть больше конечной")]
        if instance.on_moderation:
            instance.is_draft = False
        instance, errors = self.check_required_fieds(instance, request.data.get('section'), errors)
        if errors:
            raise ValidationError(errors)  
        if instance_dict != model_to_dict(instance, exclude=NOT_MODERATED_FIELDS) and instance.is_active:
            instance.is_active = False
            instance.on_moderation = True
        instance.save()
        Expert.objects.filter(pk=instance.tour_basic.expert_id).update(tours_count=F('tours_count')-1)
        if instance.on_moderation and len(instance.completed_sections) < 8:
            instance.on_moderation = False
            instance.save()
            return Response({'error': True, 'message': _('Не все обязательные поля тура заполнены')}, status=403)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(TourSerializer(instance, context={'request': request}).data, status=201)
    
    @action(['post', 'patch'], detail=True)
    def propertyimages(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_set_tour_field_for_moderation(instance, 'tour_property_images')
        if request.method == 'POST':
            instance, data = self.get_instance_image_data(request)
            image = instance.tour_property_images.create(expert=instance.tour_basic.expert, tour_basic =instance.tour_basic, **data)
            images = instance.tour_property_images.all()
            return Response(ImageSerializer(images, context={'request': request}, many=True).data, status=201)
        if request.method == 'PATCH':
            image = TourPropertyImage.objects.get(pk=request.data.get('id'))
            instance.tour_property_images.remove(image)
            return Response({}, status=204)
    
    @action(['post', 'patch'], detail=True)
    def gallary(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_set_tour_field_for_moderation(instance, 'tour_images')
        if request.method == 'POST':
            instance, data = self.get_instance_image_data(request)
            image = instance.tour_images.create(expert=instance.tour_basic.expert, tour_basic =instance.tour_basic, **data)
            images = instance.tour_images.all()           
            return Response(ImageSerializer(images, context={'request': request}, many=True).data, status=200)
        if request.method == 'PATCH':
            image = TourImage.objects.get(pk=request.data.get('id'))
            instance.tour_images.remove(image)
            return Response({}, status=204)
    
    @action(['post', 'delete'], detail=True)
    def wallpaper(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.method == 'POST':
            instance, data = self.get_instance_wallpaper_data(request)
            image = TourWallpaper.objects.create(expert=instance.tour_basic.expert, tour_basic =instance.tour_basic, **data)
            instance.wallpaper = image
            instance.save()
            return Response(WallpaperSerializer(image, context={'request': request}).data, status=201)
        if request.method == 'DELETE':
            instance.wallpaper = None
            instance.save()
            return Response({}, status=200)
    
    @action(['post'], detail=True)
    def dayimages(self, request, *args, **kwargs):
        instance, data = self.get_instance_image_data(request)
        image = TourDayImage.objects.create(expert=instance.tour_basic.expert, tour_basic =instance.tour_basic, **data)
        return Response(ImageSerializer(image, context={'request': request}).data, status=201)
    
    @action(['post'], detail=True)
    def planimages(self, request, *args, **kwargs):
        instance, data = self.get_instance_image_data(request)
        image = TourPlanImage.objects.create(expert=instance.tour_basic.expert, tour_basic =instance.tour_basic, **data)
        return Response(ImageSerializer(image, context={'request': request}).data, status=201)
    
    @action(['post'], detail=True)
    def guestguideimages(self, request, *args, **kwargs):
        instance, data = self.get_instance_image_data(request)
        image = TourGuestGuideImage.objects.create(expert=instance.tour_basic.expert, **data)
        return Response(ImageSerializer(image, context={'request': request}).data, status=201)
    
    @action(['post'], detail=True)
    def tourcopy(self, request, *args, **kwargs):
        instance = self.get_object()
        old_instance = instance
        instance.pk = None
        instance.id = None
        instance._state.adding = True
        if request.data.get('start_date'):
            instance.start_date = datetime.strptime(request.data.get('start_date'), "%Y-%m-%d").date()
            instance.finish_date = instance.start_date + timedelta(days=instance.duration - 1)
        instance.sold = None
        instance.watched = None
        instance.save()
        self.copy_tour_mtm(old_instance, instance)
        tour = Tour.objects.get(pk=instance.id)
        return Response(TourListSerializer(tour, context={'request': request}, many=False).data, status=201)
    
    @action(['get'], detail=True)
    def preview(self, request, *args, **kwargs):
        tour = self.get_object()
        # tour.tour_dates = Tour.objects.filter(tour_basic=tour.tour_basic).filter(is_active=True).filter(direct_link=False).filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start'))).only('id', 'start_date', 'finish_date')
        return Response(TourPreviewSerializer(tour, context={'request': request}, many=False).data, status=200)
    
    @action(['get'], detail=False)
    def tour_set(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs) 

    @action(['patch'], detail=True)
    def approve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.on_moderation = False
        instance.is_active = True
        instance.is_draft = False
        instance.save()
        Expert.objects.filter(pk=instance.tour_basic.expert_id).update(tours_count=F('tours_count')+1)
        ModerationResultEmailThread(instance).start()
        return Response({}, status=200)
    
    @action(['patch'], detail=True)
    def decline(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.on_moderation = False
        instance.is_active = False
        instance.is_draft = True
        instance.save()
        ModerationResultEmailThread(instance, reason=request.data.get('reason')).start()
        DeclineReason.objects.create(tour=instance, reason=request.data.get('reason'), staff=request.user)
        return Response({}, status=200)


class TourTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourType.objects.all()
    serializer_class = TourTypeSerializer

class TourPropertyTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourPropertyType.objects.all()
    serializer_class = TourPropertyTypeSerializer


class TourAccomodationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourAccomodation.objects.all()
    serializer_class = TourAccomodationSerializer

class FilterView(APIView):
    def get(self, request, format=None):
        tour_basic = TourBasic.objects.prefetch_related('expert')
        prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
        qs = Tour.objects.prefetch_related(prefetch_tour_basic, 'start_country', 'start_city', 'wallpaper', 'currency').only('id', 'name', 'start_date', 'start_country', 'start_city', 'price', 'discount', 'duration', 'tour_basic', 'wallpaper', 'vacants_number', 'currency').filter(is_active=True).filter(direct_link=False).filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start')))
        tour_types = TourType.objects.filter(Q(tours_by_basic_type__in=qs) | Q(tours_by_additional_types__in=qs)).order_by('name').values('name', 'id').distinct()      
        languages = Language.objects.filter(tours__in=qs).order_by('name').values('name', 'id').distinct()
        property_type = TourPropertyType.objects.filter(tours__in=qs).order_by('name').values('name', 'id').distinct()
        accomodation = TourAccomodation.objects.filter(tours__in=qs).order_by('name').values('name', 'id').distinct()

        filter_data = [
            {'title': 'Типы туров', 'type':'tour_types', 'data': tour_types},
            {'title': 'Языки тура', 'type':'languages', 'data': languages},
            {'title': 'Проживание', 'type':'property_type', 'data': property_type},
            {'title': 'Размещение', 'type':'accomodation', 'data': accomodation}
        ]
            
        return Response(filter_data, status=200)

class ActiveRegions(APIView):
    def get(self, request, format=None):
        tour_basic = TourBasic.objects.prefetch_related('expert')
        prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
        tours = Tour.objects.prefetch_related(prefetch_tour_basic, 'start_country', 'start_city', 'wallpaper', 'currency').only('id', 'name', 'start_date', 'start_country', 'start_city', 'price', 'discount', 'duration', 'tour_basic', 'wallpaper', 'vacants_number', 'currency').filter(is_active=True).filter(direct_link=False).filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start')))
        # regions = Region.objects.filter(tours__in=qs).order_by('name').values('name', 'id').distinct()
        country_regions = CountryRegion.objects.filter(tours_by_start_russian_region__in=tours).distinct()
        prefethed_country_regions = Prefetch('country_regions', country_regions)
        countries = Country.objects.prefetch_related(prefethed_country_regions).filter(tours_by_start_country__in=tours).distinct()
        prefethed_countries = Prefetch('countries', countries)
        regions = Region.objects.prefetch_related(prefethed_countries).filter(tours_by_start_region__in=tours).distinct()
        return Response(RegionShortSerializer(regions, many=True).data, status=200)

class ActiveCountryRegions(APIView):
    def get(self, request, format=None):
        tour_basic = TourBasic.objects.prefetch_related('expert')
        prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
        qs = Tour.objects.prefetch_related(prefetch_tour_basic, 'start_country', 'start_city', 'wallpaper', 'currency').only('id', 'name', 'start_date', 'start_country', 'start_city', 'price', 'discount', 'duration', 'tour_basic', 'wallpaper', 'vacants_number', 'currency').filter(is_active=True).filter(direct_link=False).filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start')))
        regions = Region.objects.filter(tours__in=qs).order_by('name').values('name', 'id').distinct()
        return Response(RegionShortSerializer(regions, many=True).data, status=200)