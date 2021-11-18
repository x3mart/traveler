from django_filters.filters import BaseInFilter, DateFilter, DateFromToRangeFilter, NumberFilter
from django_filters import rest_framework as filters
from tours.models import TourBasic

class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class TourFilter(filters.FilterSet):
    start_date = DateFromToRangeFilter()
    start_countries = NumberInFilter(field_name="start_country", lookup_expr='in')

    class Meta:
        model = TourBasic
        fields = ['start_date', 'start_countries', 'start_region']
