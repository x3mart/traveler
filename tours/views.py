from posixpath import split
import time
from django.db.models.query import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from tours.filters import TourFilter
from tours.mixins import TourMixin
from tours.models import Tour, TourDay, TourDayImage, TourImage, TourPropertyImage, TourType
from accounts.models import Expert
from tours.permissions import TourPermission, TourTypePermission
from tours.serializers import TourBasicSerializer, TourDayImageSerializer, TourDaySerializer, TourImageSerializer, TourListSerializer, TourPropertyImageSerializer, TourSerializer, TourTypeSerializer


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
        tour_days = TourDay.objects.prefetch_related('tour_day_images')
        prefetched_tour_days = Prefetch('tour_days', tour_days)
        if self.action == 'list':
            qs = Tour.objects.prefetch_related(prefetched_expert, 'start_country', 'currency').only('id', 'start_date', 'finish_date', 'currency', 'cost', 'price', 'discount', 'rating', 'reviews_count', 'name', 'start_country', 'expert', 'wallpaper')
        else:
            qs = Tour.objects.prefetch_related(prefetched_expert, 'start_country', 'start_city', 'start_region', 'start_russian_region', 'finish_russian_region', 'finish_country', 'finish_city', 'finish_region', 'basic_type', 'additional_types', 'tour_property_types', 'tour_property_images', 'tour_images', prefetched_tour_days, 'main_impressions', 'tour_included_services', 'tour_excluded_services', 'languages', 'currency', 'prepay_currency')  
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
        tour = Tour.objects.create(expert=self.get_expert(request), **data)
        return Response(TourSerializer(tour).data, status=201)
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        instance = self.get_object()
        instance = self.set_related_models(request, instance)
        instance = self.set_model_fields(data, instance)
        instance.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(TourSerializer(instance).data, status=201)

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

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TourPropertyImageViewSet(viewsets.ModelViewSet):
    queryset = TourPropertyImage.objects.all()
    serializer_class = TourPropertyImageSerializer
    permission_classes = [AllowAny]


class TourImageViewSet(viewsets.ModelViewSet):
    queryset = TourImage.objects.all()
    serializer_class = TourImageSerializer
    permission_classes = [AllowAny]