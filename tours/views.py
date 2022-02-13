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
from tours.models import Tour, TourDay, TourDayImage, TourType
from accounts.models import Expert
from tours.permissions import TourPermission, TourTypePermission
from tours.serializers import TourBasicSerializer, TourDayImageSerializer, TourDaySerializer, TourListSerializer, TourSerializer, TourTypeSerializer


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
            qs = Tour.objects.prefetch_related(prefetched_expert, 'start_country', 'currency').filter(is_active=True).only('id', 'start_date', 'finish_date', 'currency', 'cost', 'price', 'discount', 'rating', 'reviews_count', 'name', 'start_country', 'expert', 'wallpaper')
            return qs
        qs = Tour.objects.prefetch_related(prefetched_expert, 'start_country', 'start_city', 'start_region', 'start_russian_region', 'finish_russian_region', 'finish_country', 'finish_city', 'finish_region', 'basic_type', 'additional_types', 'tour_property_types', 'tour_property_images', 'tour_images', prefetched_tour_days, 'tour_impressions', 'tour_included_services', 'tour_excluded_services', 'languages', 'currency')        
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
        tour_basic = Tour.objects.create(expert=self.get_expert(request), **data)
        return Response(TourBasicSerializer(tour_basic).data, status=201)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = self.set_related_models(request, instance)
        instance.save()
        return super().update(request, *args, **kwargs)


class TourBasicViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourBasicSerializer
    permission_classes = [TourPermission]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'id']

    def set_additional_types(self, request, instance=None):
        if instance and instance.additional_types.exists():
            instance.additional_types.clear()
        additional_types = []
        additional_type_ids = request.data.get('additional_types').split(',')
        for additional_type_id in additional_type_ids:
            additional_types.append(TourType.objects.get(pk=additional_type_id))
        instance.additional_types.add(*tuple(additional_types))
        
    def get_basic_type(self, request):
        if request.data.get('basic_type'):
            return get_object_or_404(TourType, pk=request.data.get('basic_type'))
        return None
    
    def get_expert(self, request):
        return get_object_or_404(Expert, pk=request.user.id)

    def get_queryset(self):
        qs = Tour.objects.prefetch_related('expert', 'start_country', 'start_city')
        return qs
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        data['is_draft'] = True
        tour_basic = Tour.objects.create(expert=self.get_expert(request), basic_type = self.get_basic_type(request), **data)
        if request.data.get('additional_types'):
            self.set_additional_types(request, tour_basic)
        return Response(TourBasicSerializer(tour_basic).data, status=201)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('additional_types'):
            self.set_additional_types(request, instance)
        if self.get_basic_type(request):
            instance.basic_type = self.get_basic_type(request)
        if request.data.get('start_region'):
            instance.start_region_id = request.data.get('start_region')
        if request.data.get('finish_region'):
            instance.finish_region_id = request.data.get('finish_region')
        if request.data.get('start_country'):
            instance.start_country_id = request.data.get('start_country')
        if request.data.get('finish_country'):
            instance.finish_country_id = request.data.get('finish_country')
        if request.data.get('start_city'):
            instance.start_city_id = request.data.get('start_city')
        if request.data.get('finish_city'):
            instance.finish_city_id = request.data.get('finish_city')
        if request.data.get('team_member'):
            instance.team_member_id = request.data.get('team_member')
        instance.save()
        return super().update(request, *args, **kwargs)

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