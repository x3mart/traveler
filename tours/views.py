from posixpath import split
from django.db.models.query import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from tours.filters import TourFilter
from tours.models import TourAdvanced, TourBasic, TourType
from accounts.models import Expert
from tours.serializers import TourBasicSerializer, TourListSerializer, TourSerializer, TourTypeSerializer

# Create your views here.
class TourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourAdvanced.objects.all()
    serializer_class = TourSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['basic_tour__rating', 'id']
    filterset_class = TourFilter

    def get_queryset(self):
        expert = Expert.objects.only('id', 'first_name', 'last_name', 'about', 'rating', 'tours_count', 'tours_rating', 'reviews_count', 'tour_reviews_count', 'avatar')
        prefetched_expert = Prefetch('expert', expert)
        if self.action == 'list':
            basic_tour = TourBasic.objects.prefetch_related(prefetched_expert, 'start_country',).only('rating', 'reviews_count', 'name', 'start_country', 'expert', 'wallpaper')
            prefetched_basic_tour = Prefetch('basic_tour', basic_tour)
            qs = TourAdvanced.objects.prefetch_related(prefetched_basic_tour, 'currency').filter(basic_tour__is_active=True).only('id', 'start_date', 'finish_date', 'basic_tour', 'currency', 'cost', 'price', 'discount')
            return qs
        basic_tour = TourBasic.objects.prefetch_related(prefetched_expert, 'start_country', 'start_city', 'start_region', 'finish_country', 'finish_city', 'finish_region', 'basic_type', 'additional_types', 'tour_property_types', 'tour_property_images', 'tour_images', 'tour_days', 'tour_impressions', 'tour_included_services', 'tour_excluded_services',)
        prefetched_basic_tour = Prefetch('basic_tour', basic_tour)
        qs = TourAdvanced.objects.prefetch_related(prefetched_basic_tour, 'languages', 'currency').filter(basic_tour__is_active=True)        
        return qs
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TourListSerializer
        return super().get_serializer_class()


class TourBasicViewSet(viewsets.ModelViewSet):
    queryset = TourBasic.objects.all()
    serializer_class = TourBasicSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'id']
    # filterset_class = TourFilter

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
        qs = TourBasic.objects.prefetch_related('expert', 'start_country', 'start_city')
        return qs
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        data['is_draft'] = True
        tour_basic = TourBasic.objects.create(expert=self.get_expert(request), basic_type = self.get_basic_type(request), **data)
        if request.data.get('additional_types'):
            self.set_additional_types(request, tour_basic)
            # tour_basic.save()
        return Response(TourBasicSerializer(tour_basic).data, status=201)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('additional_types'):
            self.set_additional_types(request, instance)
        if self.get_basic_type(request):
            instance.basic_type = self.get_basic_type(request)
            instance.save()
        return super().update(request, *args, **kwargs)

class TourTypeViewSet(viewsets.ModelViewSet):
    queryset = TourType.objects.all()
    serializer_class = TourTypeSerializer
    permission_classes = [AllowAny]