from django_filters.filters import BaseInFilter, DurationFilter, BooleanFilter, DateFromToRangeFilter, NumberFilter
from django_filters import rest_framework as filters
from tours.models import Tour
from django.db.models import Q, F
from datetime import datetime

class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class TourFilter(filters.FilterSet):
    start_date = DateFromToRangeFilter(field_name='start_date')
    countries = NumberInFilter(field_name="start_country", lookup_expr='in')
    regions = NumberInFilter(field_name="start_region", lookup_expr='in')
    languages = NumberInFilter(field_name="languages", lookup_expr='in')
    types = NumberInFilter(method='types_filter', label='search_by_tour_types')
    cost_min = NumberFilter(field_name='cost', lookup_expr='gte')
    cost_max = NumberFilter(field_name='cost', lookup_expr='lte')
    discount = BooleanFilter(field_name='discount')
    duration_min = NumberFilter(field_name='duration', lookup_expr='gte')
    duration_max = NumberFilter(field_name='duration', lookup_expr='lte')
    vacants_number = NumberFilter(field_name='vacants_number', lookup_expr='gte')
    rating = NumberFilter(field_name='tour_basic__rating', lookup_expr='gte')
    difficulty = NumberFilter(field_name='difficulty_level', lookup_expr='lte')
    comfort_level = NumberFilter(field_name='comfort_level', lookup_expr='gte')

    class Meta:
        model = Tour
        fields = ['start_date', 'countries', 'regions', 'types', 'languages', 'cost_min', 'cost_max', 'discount', 'duration_min', 'duration_max', 'vacants_number', 'rating', 'difficulty']
    
    def types_filter(self, queryset, name, value):
        return queryset.filter(Q(basic_type__in=value) | Q(additional_types__in=value)).distinct()
    
    def discount_filter(self, queryset, name, value):
        queryset.filter(~Q(discount__isnull=True) and Q(discount__gt=0) and Q(discount_start_date__lte=datetime.today().date()) and Q(discount_finish_date__gte=datetime.today().date()))
        
