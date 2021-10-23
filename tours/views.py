from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from modeltranslation.utils import get_language
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Avg
from django.db.models import Count
from tours.models import TourBasic
from tours.serializers import TourBasicListSerializer, TourBasicSerializer

# Create your views here.
class TourBasicViewSet(viewsets.ModelViewSet):
    queryset = TourBasic.objects.only('name', 'start_country',).defer('expert', 'start_region', 'finish_region')
    serializer_class = TourBasicSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['tours_count', 'tours_avg_rating']
    filterset_fields = ['start_country__name', 'start_city__name']

    def get_queryset(self):
        qs = TourBasic.objects.all()
        ordering = self.request.query_params.get('ordering')
        ordering = self.request.query_params.get('limit')
        if self.action == 'list':
            qs = qs.only('name', 'start_country', 'expert',).annotate(expert_tours_count=Count('expert__tours')).annotate(expert_avg_rating=Avg('expert__expert_reviews__rating'))
        if (ordering and ordering == 'tours_avg_rating') or self.action == 'retrieve':
            qs.exclude(tour_reviews__isnull=True).annotate(tours_avg_rating=Avg('tour_reviews__rating'))
        return qs
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TourBasicListSerializer
        return super().get_serializer_class()
    
    def get_serializer_context(self):
        context = super(TourBasicViewSet, self).get_serializer_context()
        context.update({"language": get_language()})
        return context