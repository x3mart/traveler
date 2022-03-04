from rest_framework.decorators import action
import time
from django.db.models.query import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.forms.models import model_to_dict
from tours.filters import TourFilter
from tours.mixins import TourMixin, NOT_MODERATED_FIELDS
from tours.models import Tour, TourAccomodation, TourBasic, TourDayImage, TourGuestGuideImage, TourImage, TourPlanImage, TourPropertyImage, TourPropertyType, TourType
from tours.permissions import TourPermission
from tours.serializers import ImageSerializer, TourAccomodationSerializer, TourDayImageSerializer, TourGuestGuideImageSerializer, TourImageSerializer, TourListSerializer, TourPlanImageSerializer, TourPropertyImageSerializer, TourPropertyTypeSerializer, TourSerializer, TourTypeSerializer


# Create your views here.
class TourViewSet(viewsets.ModelViewSet, TourMixin):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [TourPermission]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'id']
    filterset_class = TourFilter

    def get_queryset(self):
        tour_basic = TourBasic.objects.all()
        prefetched_tour_basic = Prefetch('tour_basic', tour_basic)
        if self.action == 'list':
            qs = Tour.objects.prefetch_related(prefetched_tour_basic, 'start_country', 'currency').only('id', 'name', 'start_date', 'finish_date', 'start_country', 'price', 'cost', 'discount', 'on_moderation', 'is_active', 'is_draft', 'duration', 'sold', 'watched', 'currency', 'tour_basic', 'wallpaper').filter(tour_basic__expert_id=self.request.user.id)
        else:
            qs = Tour.objects.prefetch_related(prefetched_tour_basic, 'start_country', 'start_city', 'start_region', 'start_russian_region', 'finish_russian_region', 'finish_country', 'finish_city', 'finish_region', 'basic_type', 'additional_types', 'tour_property_types', 'tour_property_images', 'tour_images', 'languages', 'currency', 'prepay_currency', 'accomodation')  
        return qs
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TourListSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        data['is_draft'] = True
        tour_basic = TourBasic.objects.create(expert=self.get_expert(request))
        tour = Tour.objects.create(tour_basic=tour_basic, **data)
        return Response(TourSerializer(tour).data, status=201)
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        instance = self.get_object()
        instance_dict = model_to_dict(instance, exclude=NOT_MODERATED_FIELDS)
        instance = self.set_mtm_fields(request, instance)
        instance = self.set_model_fields(data, instance)    
        if instance_dict != model_to_dict(instance, exclude=NOT_MODERATED_FIELDS) and instance.is_active:
            instance.is_active = False
            instance.on_moderation = True
        instance.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(TourSerializer(instance, context={'request': request}).data, status=201)
    
    @action(['post'], detail=True)
    def propertyimages(self, request, *args, **kwargs):
        instance, data = self.get_instance_image_data(request)
        image = instance.tour_property_images.create(expert=instance.tour_basic.expert, tour_basic =instance.tour_basic, **data)
        return Response(ImageSerializer(image, context={'request': request}).data, status=201)
    
    @action(['post'], detail=True)
    def gallary(self, request, *args, **kwargs):
        instance, data = self.get_instance_image_data(request)
        image = instance.tour_images.create(expert=instance.tour_basic.expert, tour_basic =instance.tour_basic, **data)
        return Response(ImageSerializer(image, context={'request': request}).data, status=201)
    
    @action(['post'], detail=True)
    def dayimages(self, request, *args, **kwargs):
        instance, data = self.get_instance_image_data(request)
        image = TourDayImage.objects.create(expert=instance.tour_basic.expert, tour_basic =instance.tour_basic, **data)
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
        instance.sold = None
        instance.watched = None
        instance.save()
        self.copy_tour_mtm(old_instance, instance)
        return Response(TourSerializer(instance, context={'request': request}).data, status=201)

class TourTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourType.objects.all()
    serializer_class = TourTypeSerializer
    # permission_classes = [TourTypePermission]


class TourDayImageViewSet(viewsets.ModelViewSet):
    queryset = TourDayImage.objects.all()
    serializer_class = TourDayImageSerializer


class TourPlanImageViewSet(viewsets.ModelViewSet):
    queryset = TourPlanImage.objects.all()
    serializer_class = TourPlanImageSerializer


class TourGuestGuideImageViewSet(viewsets.ModelViewSet):
    queryset = TourGuestGuideImage.objects.all()
    serializer_class = TourGuestGuideImageSerializer


class TourPropertyTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourPropertyType.objects.all()
    serializer_class = TourPropertyTypeSerializer


class TourPropertyImageViewSet(viewsets.ModelViewSet):
    queryset = TourPropertyImage.objects.all()
    serializer_class = TourPropertyImageSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        tour = Tour.objects.get(pk=request.data.get('tour'))
        instance = tour.tour_property_images.create(**data)
        return Response(TourPropertyImageSerializer(instance, context={'request': request}).data, status=201)


class TourImageViewSet(viewsets.ModelViewSet):
    queryset = TourImage.objects.all()
    serializer_class = TourImageSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        tour = Tour.objects.get(pk=request.data.get('tour'))
        instance = tour.tour_images.create(**data)
        return Response(TourImageSerializer(instance, context={'request': request}).data, status=201)


class TourAccomodationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourAccomodation.objects.all()
    serializer_class = TourAccomodationSerializer