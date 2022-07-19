from datetime import timedelta, datetime
from django.forms import DurationField
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.db.models.query import Prefetch
from django.db.models import Q, F, Case, Count, When, Value, BooleanField
from django.db.models.lookups import GreaterThan
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
from accounts.models import Expert, Identifier, RecentlyViewedTour
from accounts.serializers import ExpertListSerializer
from currencies.models import Currency
from geoplaces.models import Destination, Destination, Region
from geoplaces.serializers import DestinationSerializer, RegionSerializer, RegionShortSerializer
from reviews.models import TourReview
from reviews.serializers import TourReviewSerializer
from tours.filters import TourFilter
from tours.mixins import TourMixin
from tours.paginations import TourResultsSetPagination
from utils.constants import NOT_MODERATED_FIELDS
from tours.models import DeclineReason, Tour, TourAccomodation, TourBasic, TourDayImage, TourGuestGuideImage, TourImage, TourPlanImage, TourPropertyImage, TourPropertyType, TourType, TourWallpaper
from tours.permissions import TourPermission
from tours.serializers import FilterSerializer, ImageSerializer, TourAccomodationSerializer, TourListSerializer, TourPreviewSerializer, TourPropertyTypeSerializer, TourSerializer, TourTypeSerializer, TourTypeShortSerializer, WallpaperSerializer, TourSetSerializer
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


class TourViewUpdate(threading.Thread):
    def __init__(self, tour, ident):
        self.user = tour.tour_basic.expert
        self.tour = tour
        self.ident = ident
        threading.Thread.__init__(self)
    
    def run(self):
        identifier = Identifier.objects.get(pk=self.ident)
        recently, created = RecentlyViewedTour.objects.get_or_create(tour_id=self.tour.id, user_uuid_id=self.ident)
        recently.viewed_at = datetime.now()
        recently.save()
        if created:
            Tour.objects.filter(pk=self.tour.id).update(views_count=F('views_count')+1)
        if self.tour.start_destination not in identifier.viewed_destinations.all():
            Destination.objects.filter(pk=self.tour.start_destination.id).update(views_count=F('views_count')+1)

# Create your views here.
class TourViewSet(viewsets.ModelViewSet, TourMixin):
    queryset = Tour.objects.prefetched().with_discounted_price().distinct()
    serializer_class = TourSerializer
    permission_classes = [TourPermission]
    pagination_class = TourResultsSetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'id']
    ordering = ['start_date']
    filterset_class = TourFilter

    def get_queryset(self):
        if self.action in ['list',]:
            qs = super().get_queryset().in_sale()
            if self.request.auth:
                favorite_tours_ids = self.request.user.favorite_tours.values_list('id', flat=True)
                qs = qs.annotate(is_favorite=Case(
                    When(Q(id__in=favorite_tours_ids), then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField())
                )
            else:
                qs = qs.annotate(is_favorite = Value(False))
        elif self.action in ['preview',]:
            qs = super().get_queryset()
            if self.request.auth:
                favorite_tours_ids = self.request.user.favorite_tours.values_list('id', flat=True)
                qs = qs.annotate(is_favorite=Case(
                    When(Q(id__in=favorite_tours_ids), then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField())
                )
            else:
                qs = qs.annotate(is_favorite = Value(False))            
        elif self.action in ['tour_set',]:
            qs = super().get_queryset().filter(tour_basic__expert_id=self.request.user.id).order_by('-id')
        else:
            qs = super().get_queryset()
        return qs
    
    def get_serializer_class(self):
        if self.action in ['tour_set',]:
            return TourSetSerializer
        elif self.action in ['preview',]:
            return TourPreviewSerializer
        elif  self.action in ['list', 'types']:
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
        instance.views_count = None
        instance.save()
        self.copy_tour_mtm(old_instance, instance)
        tour = Tour.objects.get(pk=instance.id)
        return Response(TourListSerializer(tour, context={'request': request}, many=False).data, status=201)
    
    @action(['get'], detail=True, lookup_field='slug')
    def preview(self, request, *args, **kwargs):
        qs = self.get_queryset()
        slug = kwargs.get('pk')
        id = request.query_params.get('date_id')
        if id:
            tour = qs.get(pk=id)
        else:
            tours = qs.filter(slug=slug).in_sale().order_by('start_date')
            if tours.exists():
                tour = tours.first()
                tour.archive = False
            else:
                tour = qs.filter(slug=slug).actives().order_by('-start_date').first()
                tour.archive = True
        tour.tour_dates = Tour.objects.in_sale().only('id', 'start_date', 'finish_date')
        ident = request.query_params.get('ident')
        # if ident:
        #     TourViewUpdate(tour, ident).start()
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
    
    @action(['patch', 'delete'], detail=True)
    def favorite(self, request, *args, **kwargs):
        tour = self.get_object()
        if request.method == 'PATCH':
            if not (hasattr(request.user, 'favorite_tours') and request.user.favorite_tours.filter(id = tour.id).exists()):
                request.user.favorite_tours.add(tour)
            return Response({}, status=204)
        if request.method == 'DELETE':
            if hasattr(request.user, 'favorite_tours'):
                request.user.favorite_tours.remove(tour)
            return Response({}, status=204)

    @action(['get'], detail=False)
    def favorites(self, request, *args, **kwargs):
        tours = request.user.favorite_tours.prefetched().with_discounted_price().annotate(is_favorite = Value(True)).all()
        return Response(TourListSerializer(tours, many=True, context={'request':request}).data, status=200)



class TourTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourType.objects.all()
    serializer_class = TourTypeSerializer

class TourPropertyTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourPropertyType.objects.all()
    serializer_class = TourPropertyTypeSerializer


class TourAccomodationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourAccomodation.objects.all()
    serializer_class = TourAccomodationSerializer

# class FilterView(APIView):
#     def get(self, request, format=None):
#         tour_basic = TourBasic.objects.prefetch_related('expert')
#         prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
#         qs = Tour.objects.prefetch_related(prefetch_tour_basic, 'start_destination', 'start_city', 'wallpaper', 'currency').only('id', 'name', 'start_date', 'start_destination', 'start_city', 'price', 'discount', 'duration', 'tour_basic', 'wallpaper', 'vacants_number', 'currency').filter(is_active=True).filter(direct_link=False).filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start')))
#         tour_types = TourType.objects.filter(Q(tours_by_basic_type__in=qs) | Q(tours_by_additional_types__in=qs)).order_by('name').values('name', 'id').distinct()      
#         languages = Language.objects.filter(tours__in=qs).order_by('name').values('name', 'id').distinct()
#         property_type = TourPropertyType.objects.filter(tours__in=qs).order_by('name').values('name', 'id').distinct()
#         accomodation = TourAccomodation.objects.filter(tours__in=qs).order_by('name').values('name', 'id').distinct()

#         filter_data = [
#             {'title': 'Типы туров', 'type':'tour_types', 'data': tour_types},
#             {'title': 'Языки тура', 'type':'languages', 'data': languages},
#             {'title': 'Проживание', 'type':'property_type', 'data': property_type},
#             {'title': 'Размещение', 'type':'accomodation', 'data': accomodation}
#         ]
            
#         return Response(filter_data, status=200)

class ActiveRegion(APIView):
    def get(self, request, format=None):
        tours = Tour.objects.in_sale()
        # regions = Region.objects.filter(tours__in=qs).order_by('name').values('name', 'id').distinct()
        destinations = Destination.objects.filter(tours_by_start_destination__in=tours).distinct()
        prefethed_destinations = Prefetch('destinations', destinations)
        regions = Region.objects.prefetch_related(prefethed_destinations).filter(tours_by_start_region__in=tours).annotate(tours_count=Count('tours_by_start_region')).order_by('name').distinct()
        return Response(RegionSerializer(regions, many=True).data, status=200)

class ActiveDestination(APIView):
    def get(self, request, format=None):
        tours = Tour.objects.in_sale()
        destinations = Destination.objects.filter(tours_by_start_destination__in=tours).distinct().prefetch_related('region').annotate(tours_count=Count('tours_by_start_destination')).order_by('name').distinct()
        return Response(DestinationSerializer(destinations, many=True, context={'request':request}).data, status=200)

class ActiveType(APIView):
    def get(self, request, format=None):
        tours = Tour.objects.in_sale()
        types = TourType.objects.filter(Q(tours_by_basic_type__in=tours) | Q(tours_by_additional_types__in=tours)).annotate(tours_count=Count('tours_by_basic_type', filter=Q(tours_by_basic_type__in=tours), distinct=True) + Count('tours_by_additional_types', filter=Q(tours_by_additional_types__in=tours), distinct=True)).distinct()
        return Response(TourTypeSerializer(types, many=True, context={'request':request}).data, status=200)

class StartPage(APIView):
    def get(self, request, format=None):
        queryset = Tour.objects.in_sale()
        new = queryset.prefetched().with_discounted_price().order_by('tour_basic__created_at', 'start_date').distinct('tour_basic__created_at')[:5]
        popular = Destination.objects.filter(tours_by_start_destination__in=queryset).distinct().prefetch_related('region').annotate(tours_count=Count('tours_by_start_destination')).order_by('-views_count')[:12]
        regions = Region.objects.filter(tours_by_start_region__in=queryset).distinct()
        types = TourType.objects.filter(Q(tours_by_basic_type__in=queryset) | Q(tours_by_additional_types__in=queryset)).annotate(tours_count=Count('tours_by_basic_type', filter=Q(tours_by_basic_type__in=queryset), distinct=True) + Count('tours_by_additional_types', filter=Q(tours_by_additional_types__in=queryset), distinct=True)).distinct()
        rated = queryset.prefetched().with_discounted_price().order_by('-tour_basic__rating', 'start_date').distinct()[:5]
        experts = Expert.objects.annotate(active_tours = Count('tours__tours', filter=(Q(tours__tours__booking_delay__lte=F('tours__tours__start_date') - datetime.today().date() - F('tours__tours__postpay_days_before_start'))))).filter(active_tours__gt=0).order_by('-rating')[:6]
        discounted = queryset.prefetched().with_discounted_price().annotate(d = (F('price') - F('discounted_price'))).filter(d__gt=0).order_by('-d')[:5]
        reviews = TourReview.objects.filter(is_active=True).order_by('-id')[:4]
        start_page = {
            'new':TourListSerializer(new, many=True, context={'request':request}).data,
            'popular':DestinationSerializer(popular, many=True, context={'request':request}).data,
            'regions':RegionSerializer(regions, many=True, context={'request':request}).data,
            'types':TourTypeSerializer(types[:6], many=True, context={'request':request}).data,
            'rated':TourListSerializer(rated, many=True, context={'request':request}).data,
            'discounted':TourListSerializer(discounted, many=True, context={'request':request}).data,
            'experts':ExpertListSerializer(experts, many=True, context={'request':request}).data,
            'reviews':TourReviewSerializer(reviews, many=True, context={'request':request}).data,
            'types_all':TourTypeSerializer(types, many=True, context={'request':request}).data
        }
        return Response(start_page, status=200) 


class MainMenu(APIView):
    def get(self, request, format=None):
        menu = [
            {
                'title': 'Путешествия',
                'submenu': [
                    {'title': 'Все путешествия', 'url':'/tours'},
                    {'title': 'Все регионы', 'url':'/regions'},
                    {'title': 'Все направления', 'url':'/destinations'},
                    {'title': 'Все типы туров', 'url':'/destinations'},
                    {'title': 'Статьи о путешествиях', 'url':'/articles'},
                    {'title': 'Блоги о путешествиях', 'url':'/blogs'},
                ]
            },
            {
                'title': 'Поддержка',
                'submenu': [
                    {'title': 'ЧаВо', 'url':'/faqs'},
                    {'title': 'Чат с тех поддержкой', 'url':'/account/support'},
                ]
            }
        ]
    
        return Response(menu, status=200)