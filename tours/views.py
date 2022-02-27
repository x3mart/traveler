from posixpath import split
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
from tours.models import Tour, TourBasic, TourDay, TourDayImage, TourImage, TourPlan, TourPropertyImage, TourPropertyType, TourType
from accounts.models import Expert
from tours.permissions import TourPermission, TourTypePermission
from tours.serializers import TourBasicSerializer, TourDayImageSerializer, TourDaySerializer, TourImageSerializer, TourListSerializer, TourPlanSerializer, TourPropertyImageSerializer, TourPropertyTypeSerializer, TourSerializer, TourTypeSerializer


# Create your views here.
class TourViewSet(viewsets.ModelViewSet, TourMixin):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [TourPermission]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'id']
    filterset_class = TourFilter

    def get_queryset(self):
        expert = Expert.objects.only('id', 'first_name', 'last_name', 'about', 'rating', 'tours_count', 'tours_rating', 'reviews_count', 'tour_reviews_count', 'avatar')
        prefetched_expert = Prefetch('expert', expert)
        tour_basic = TourBasic.objects.prefetch_related(prefetched_expert)
        prefetched_tour_basic = Prefetch('tour_basic', tour_basic)
        tour_days = TourDay.objects.prefetch_related('tour_day_images')
        prefetched_tour_days = Prefetch('tour_days', tour_days)
        if self.action == 'list':
            qs = Tour.objects.prefetch_related(prefetched_tour_basic, 'start_country', 'currency').filter(tour_basic__expert_id=self.request.user.id)
        else:
            qs = Tour.objects.prefetch_related(prefetched_tour_basic, 'start_country', 'start_city', 'start_region', 'start_russian_region', 'finish_russian_region', 'finish_country', 'finish_city', 'finish_region', 'basic_type', 'additional_types', 'tour_property_types', 'tour_property_images', 'tour_images', prefetched_tour_days, 'main_impressions', 'tour_included_services', 'tour_excluded_services', 'languages', 'currency', 'prepay_currency', 'accomodation')  
        return qs
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TourListSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        data['is_draft'] = True
        tour_basic = TourBasic.objects.create(expert=self.get_expert(request))
        tour = Tour.objects.create(tour_basic=tour_basic, **data)
        return Response(TourSerializer(tour).data, status=201)
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        instance = self.get_object()
        instance_dict = model_to_dict(instance)
        instance, updated_mtm_fields = self.set_mtm_fields(request, instance)
        instance, updated_model_fields = self.set_model_fields(data, instance)
        updated_fields = set(updated_mtm_fields + updated_model_fields)
        # print(instance_dict)      
        # print(instance_dict == model_to_dict(instance, exclude=NOT_MODERATED_FIELDS))      
        if instance_dict == model_to_dict(instance, exclude=NOT_MODERATED_FIELDS) and instance.is_active:
            instance.is_active = False
            instance.on_moderation = True
        instance.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(TourSerializer(instance, context={'request': request}).data, status=201)

class TourTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourType.objects.all()
    serializer_class = TourTypeSerializer
    # permission_classes = [TourTypePermission]

class TourDayViewSet(viewsets.ModelViewSet):
    queryset = TourDay.objects.all()
    serializer_class = TourDaySerializer


class TourDayImageViewSet(viewsets.ModelViewSet):
    queryset = TourDayImage.objects.all()
    serializer_class = TourDayImageSerializer


class TourPlanViewSet(viewsets.ModelViewSet):
    queryset = TourPlan.objects.all()
    serializer_class = TourPlanSerializer


class TourPropertyTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourPropertyType.objects.all()
    serializer_class = TourPropertyTypeSerializer


class TourPropertyImageViewSet(viewsets.ModelViewSet):
    queryset = TourPropertyImage.objects.all()
    serializer_class = TourPropertyImageSerializer
    permission_classes = [AllowAny]


class TourImageViewSet(viewsets.ModelViewSet):
    queryset = TourImage.objects.all()
    serializer_class = TourImageSerializer
    permission_classes = [AllowAny]