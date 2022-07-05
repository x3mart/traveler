from django_filters.filters import BaseInFilter, DurationFilter, BooleanFilter, DateFromToRangeFilter, NumberFilter
from django_filters import rest_framework as filters
from tours.models import Tour
from django.db.models import Q, F, Case, Value, When
from datetime import datetime

class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class TourFilter(filters.FilterSet):
    start_date = DateFromToRangeFilter(field_name='start_date')
    countries = NumberInFilter(field_name="start_country", lookup_expr='in')
    regions = NumberInFilter(field_name="start_region", lookup_expr='in')
    languages = NumberInFilter(field_name="languages", lookup_expr='in')
    tour_types = NumberInFilter(method='tour_types_filter', label='search_by_tour_types')
    price = NumberInFilter(method='price_filter', label='Цена')
    discount = BooleanFilter(field_name='discount', method='discount_filter')
    duration = NumberInFilter(method='duration_filter', label='Продолжительность')
    vacants_number = NumberInFilter(method='vacants_number_filter', label='Свободные места')
    rating = NumberFilter(method='rating_filter', label='Рейтинг')
    expert = NumberFilter(field_name='tour_basic__expert', lookup_expr='gte')
    difficulty_level = NumberFilter(field_name='difficulty_level', lookup_expr='lte')
    comfort_level = NumberFilter(field_name='comfort_level', lookup_expr='gte')
    age = NumberInFilter(method='age_filter', label='Допустимый возраст')

    class Meta:
        model = Tour
        fields = ['start_date', 'countries', 'regions', 'tour_types', 'languages', 'price', 'discount', 'duration',  'vacants_number', 'rating', 'difficulty_level', 'age']
    
    def tour_types_filter(self, queryset, name, value):
        return queryset.filter(Q(basic_type__in=value) | Q(additional_types__in=value)).distinct()
    
    def discount_filter(self, queryset, name, value):
        if value:
            return queryset.filter(~Q(discount__isnull=True) and Q(discount__gt=0) and Q(discount_starts__lte=datetime.today().date()) and Q(discount_finish__gte=datetime.today().date()))
        else:
            return queryset
    
    def price_filter(self, queryset, name, value):
        if len(value) < 2:
            return queryset
        return queryset.filter(discounted_price__gte=value[0]).filter(discounted_price__lte=value[1])
    
    def age_filter(self, queryset, name, value):
        if len(value) < 2:
            return queryset
        return queryset.filter(age_starts__lte=value[0]).filter(age_ends__gte=value[1])
    
    def duration_filter(self, queryset, name, value):
        if len(value) < 2:
            return queryset
        return queryset.filter(duration__gte=value[0]).filter(duration__lte=value[1])
    
    def vacants_number_filter(self, queryset, name, value):
        if len(value) < 2:
            return queryset
        return queryset.filter(vacants_number__gte=value[0]).filter(vacants_number__lte=value[1])
    
    def rating_filter(self, queryset, name, value):
        if len(value) < 1:
            return queryset
        return queryset.filter(basic_tour__rating__gte=value[0])
        
