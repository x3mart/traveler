from django_filters.filters import BaseInFilter, DateFilter, DateFromToRangeFilter, NumberFilter
from django_filters import rest_framework as filters
from tours.models import TourAdvanced, TourBasic

class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class TourFilter(filters.FilterSet):
    start_date = DateFromToRangeFilter(field_name='start_date')
    countries = NumberInFilter(field_name="basic_tour__start_country", lookup_expr='in')
    regions = NumberInFilter(field_name="basic_tour__start_region", lookup_expr='in')

    class Meta:
        model = TourAdvanced
        fields = ['start_date', 'countries', 'regions']
