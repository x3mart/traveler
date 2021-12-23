from django_filters.filters import BaseInFilter, DurationFilter, BooleanFilter, DateFromToRangeFilter, NumberFilter
from django_filters import rest_framework as filters
from tours.models import TourAdvanced, TourBasic
from django.db.models import Q

class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class TourFilter(filters.FilterSet):
    start_date = DateFromToRangeFilter(field_name='start_date')
    countries = NumberInFilter(field_name="basic_tour__start_country", lookup_expr='in')
    regions = NumberInFilter(field_name="basic_tour__start_region", lookup_expr='in')
    languages = NumberInFilter(field_name="languages", lookup_expr='in')
    types = NumberInFilter(method='types_filter', label='search_by_tour_types')
    cost_min = NumberFilter(field_name='cost', lookup_expr='gte')
    cost_max = NumberFilter(field_name='cost', lookup_expr='lte')
    discount = BooleanFilter(field_name='discount', lookup_expr='isnull', exclude=True)
    duration_min = NumberFilter(field_name='duration', lookup_expr='gte')
    duration_max = NumberFilter(field_name='duration', lookup_expr='lte')
    vacants_number = NumberFilter(field_name='vacants_number', lookup_expr='gte')

    class Meta:
        model = TourAdvanced
        fields = ['start_date', 'countries', 'regions', 'types', 'languages', 'cost_min', 'cost_max', 'discount', 'duration_min', 'duration_max', 'vacants_number']
    
    def types_filter(self, queryset, name, value):
        return TourAdvanced.objects.filter(Q(basic_tour__basic_type__in=value) | Q(basic_tour__additional_types__in=value)).distinct()
