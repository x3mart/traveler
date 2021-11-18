from django.db.models.query import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from modeltranslation.utils import get_language
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Avg
from django.db.models import Count
from tours.filters import TourFilter
from tours.models import TourBasic
from accounts.models import Expert
from tours.serializers import TourBasicListSerializer, TourBasicSerializer

# Create your views here.
class TourBasicViewSet(viewsets.ModelViewSet):
    queryset = TourBasic.objects.all()
    serializer_class = TourBasicSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'id']
    filterset_class = TourFilter

    def get_queryset(self):
        experts = Expert.objects.annotate(expert_tours_count=Count('tours')).only('first_name', 'last_name', 'rating', 'avatar')
        prefetched_expert = Prefetch('expert', experts)
        qs = TourBasic.objects.prefetch_related(prefetched_expert, 'start_country', 'start_city')
        return qs
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TourBasicListSerializer
        return super().get_serializer_class()
    
    def get_serializer_context(self):
        context = super(TourBasicViewSet, self).get_serializer_context()
        context.update({"language": get_language()})
        return context


# class TourAdvancedViewSet(viewsets.ModelViewSet):
#     queryset = TourBasic.objects.all()
#     serializer_class = TourBasicSerializer
#     permission_classes = [AllowAny]
#     filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
#     ordering_fields = ['rating', 'id']
#     filterset_class = TourFilter

#     def get_queryset(self):
#         experts = Expert.objects.annotate(expert_tours_count=Count('tours')).only('first_name', 'last_name', 'rating', 'avatar')
#         prefetched_expert = Prefetch('expert', experts)
#         basic = TourBasic.objects.prefetch_related(prefetched_expert, 'start_country', 'start_city')
#         return qs
    
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return TourBasicListSerializer
#         return super().get_serializer_class()
    
#     def get_serializer_context(self):
#         context = super(TourBasicViewSet, self).get_serializer_context()
#         context.update({"language": get_language()})
#         return context