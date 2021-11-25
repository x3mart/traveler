from django.db.models.query import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from tours.filters import TourFilter
from tours.models import TourAdvanced, TourBasic
from accounts.models import Expert
from tours.serializers import TourListSerializer, TourSerializer

# Create your views here.
class TourViewSet(viewsets.ModelViewSet):
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
            qs = TourAdvanced.objects.prefetch_related(prefetched_basic_tour, 'currency').filter(basic_tour__is_active=True).only('id', 'start_date', 'finish_date', 'basic_tour', 'currency')
            return qs
        basic_tour = TourBasic.objects.prefetch_related(prefetched_expert, 'start_country', 'start_city', 'start_region', 'finish_country', 'finish_city', 'finish_region', 'basic_type', 'additional_types', 'tour_property_types', 'tour_property_images', 'tour_images', 'tour_days', 'tour_impressions', 'tour_included_services', 'tour_excluded_services',)
        prefetched_basic_tour = Prefetch('basic_tour', basic_tour)
        qs = TourAdvanced.objects.prefetch_related(prefetched_basic_tour, 'languages', 'currency').filter(basic_tour__is_active=True)        
        return qs
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TourListSerializer
        return super().get_serializer_class()


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