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
    types = NumberInFilter(method='types_filter', label='search_by_tour_types')
    price_min = NumberFilter(method='price_min_filter', label='цена мин')
    price_max = NumberFilter(method='price_max_filter', label='цена макс')
    discount = BooleanFilter(field_name='discount', method='discount_filter')
    duration_min = NumberFilter(field_name='duration', lookup_expr='gte')
    duration_max = NumberFilter(field_name='duration', lookup_expr='lte')
    vacants_number = NumberFilter(field_name='vacants_number', lookup_expr='gte')
    rating = NumberFilter(field_name='tour_basic__rating', lookup_expr='gte')
    expert = NumberFilter(field_name='tour_basic__expert', lookup_expr='gte')
    difficulty = NumberFilter(field_name='difficulty_level', lookup_expr='lte')
    comfort_level = NumberFilter(field_name='comfort_level', lookup_expr='gte')
    age_starts = NumberFilter(field_name='age_starts', lookup_expr='lte')
    age_ends = NumberFilter(field_name='age_ends', lookup_expr='gte')

    class Meta:
        model = Tour
        fields = ['start_date', 'countries', 'regions', 'types', 'languages', 'cost_min', 'cost_max', 'discount', 'duration_min', 'duration_max', 'vacants_number', 'rating', 'difficulty', 'age_starts', 'age_ends']
    
    def types_filter(self, queryset, name, value):
        return queryset.filter(Q(basic_type__in=value) | Q(additional_types__in=value)).distinct()
    
    def discount_filter(self, queryset, name, value):
        if value:
            return queryset.filter(~Q(discount__isnull=True) and Q(discount__gt=0) and Q(discount_starts__lte=datetime.today().date()) and Q(discount_finish__gte=datetime.today().date()))
        else:
            return queryset
    
    def price_min_filter(self, queryset, name, value):
        return queryset.annotate(
            discounted_price = Case(
                When(Q(discount__is_null=True) | Q(discount=0), then=F('price')),
                When(~Q(discount__is_null=True) and Q(discount__gt=0) and Q(discount_starts__lte=datetime.today().date()) and Q(discount_finish__gte=datetime.today().date()) and Q(discount_in_prc=True), then=F('price') - F('price')*F('discount')/100),
                When(~Q(discount__is_null=True) and Q(discount__gt=0) and Q(discount_starts__lte=datetime.today().date()) and Q(discount_finish__gte=datetime.today().date()) and Q(discount_in_prc=False), then=F('price') - F('discount')),
            )
        ).filter(discounted_price__gte=value)
    
    def price_max_filter(self, queryset, name, value):
        return queryset.annotate(
            discounted_price = Case(
                When(Q(discount__is_null=True) | Q(discount=0), then=F('price')),
                When(~Q(discount__is_null=True) and Q(discount__gt=0) and Q(discount_starts__lte=datetime.today().date()) and Q(discount_finish__gte=datetime.today().date()) and Q(discount_in_prc=True), then=F('price') - F('price')*F('discount')/100),
                When(~Q(discount__is_null=True) and Q(discount__gt=0) and Q(discount_starts__lte=datetime.today().date()) and Q(discount_finish__gte=datetime.today().date()) and Q(discount_in_prc=False), then=F('price') - F('discount')),
            )
        ).filter(discounted_price__lte=value)


        
        
