from django.db.models import F, Q
from datetime import timedelta, datetime
from django.forms import DurationField
from rest_framework.decorators import action
from django.db.models.query import Prefetch
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError
from currencies.models import Currency
from tours.filters import TourFilter
from tours.mixins import TourMixin, NOT_MODERATED_FIELDS, TOUR_REQUIRED_FIELDS
from tours.models import Important, ImportantTitle, Tour, TourAccomodation, TourBasic, TourDayImage, TourGuestGuideImage, TourImage, TourPlanImage, TourPropertyImage, TourPropertyType, TourType, TourWallpaper
from tours.permissions import TourPermission
from tours.serializers import ImageSerializer, TourAccomodationSerializer, TourListSerializer, TourPreviewSerializer, TourPropertyTypeSerializer, TourSerializer, TourTypeSerializer, WallpaperSerializer, TourSetSerializer


# Create your views here.
class TourViewSet(viewsets.ModelViewSet, TourMixin):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [TourPermission]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'id']
    ordering = ['start_date']
    filterset_class = TourFilter

    def get_queryset(self):
        if self.action in ['list',]:
            tour_basic = TourBasic.objects.prefetch_related('expert')
            prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
            qs = Tour.objects.prefetch_related(prefetch_tour_basic, 'start_country', 'start_city', 'wallpaper', 'currency').only('id', 'name', 'start_date', 'start_country', 'start_city', 'price', 'discount', 'duration', 'tour_basic', 'wallpaper', 'vacants_number', 'currency').filter(is_active=True).filter(tour_basic__direct_link=False).filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start')))
        elif self.action in ['tour_set',]:
            qs = Tour.objects.prefetch_related('tour_basic', 'start_country', 'currency').only('id', 'name', 'start_date', 'finish_date', 'start_country', 'price', 'cost', 'discount', 'on_moderation', 'is_active', 'is_draft', 'duration', 'sold', 'watched', 'currency', 'tour_basic', 'wallpaper').filter(tour_basic__expert_id=self.request.user.id).order_by('-id')
        else:
            qs = Tour.objects.prefetch_related('tour_basic', 'start_country', 'start_city', 'start_region', 'start_russian_region', 'finish_russian_region', 'finish_country', 'finish_city', 'finish_region', 'basic_type', 'additional_types', 'tour_property_types', 'tour_property_images', 'tour_images', 'languages', 'currency', 'prepay_currency', 'accomodation',)  
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
        return super().retrieve(request, *args, **kwargs)
    
    @action(['get'], detail=False)
    def tour_set(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)    

class TourTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourType.objects.all()
    serializer_class = TourTypeSerializer

class TourPropertyTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourPropertyType.objects.all()
    serializer_class = TourPropertyTypeSerializer


class TourAccomodationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourAccomodation.objects.all()
    serializer_class = TourAccomodationSerializer