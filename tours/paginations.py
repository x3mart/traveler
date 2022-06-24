from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import F, Q, Max, Min

from languages.models import Language
from orders.models import Order
from tours.models import TourAccomodation, TourBasic, TourPropertyType, TourType

class TourResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data,
            'filter_set': self.filter_data
        })
    
    def paginate_queryset(self, queryset, request, view=None):
        self.filter_data = self.get_filter_data(queryset, request)
        return super().paginate_queryset(queryset, request, view)
    
    def get_filter_data(self, queryset, request):
        tour_types = TourType.objects.filter(Q(tours_by_basic_type__in=queryset) | Q(tours_by_additional_types__in=queryset)).order_by('name').values('name', 'id').distinct()      
        languages = Language.objects.filter(tours__in=queryset).order_by('name').values('name', 'id').distinct()
        property_type = TourPropertyType.objects.filter(tours__in=queryset).order_by('name').values('name', 'id').distinct()
        accomodation = TourAccomodation.objects.filter(tours__in=queryset).order_by('name').values('name', 'id').distinct()
        aggregations = queryset.aggregate(Min('discounted_price'), Max('discounted_price'), Min('age_starts'), Max('age_ends'), Min('duration'), Max('duration'),  Max('vacants_number'), Max('tour_basic__rating'), Max('difficulty_level'), Max('comfort_level'))
        TourBasic.objects.filter(tours__in=queryset).aggregate(Max('rating'))
        filter_data = [
            {'title': 'Тип тура', 'type':'tour_types', 'data': tour_types},
            {'title': 'Языки группы', 'type':'languages', 'data': languages},
            {'title': 'Проживание', 'type':'property_type', 'data': property_type},
            {'title': 'Размещение', 'type':'accomodation', 'data': accomodation},
            {'title': 'Цена', 'type':'price', 'filter_type': 'range', 'data': [aggregations['discounted_price__min'], aggregations['discounted_price__max']]},
            {'title': 'Допустимый возраст', 'type':'age', 'filter_type': 'range', 'data': [aggregations['age_starts__min'], aggregations['age_ends__max']]},
            {'title': 'Продолжительность тура', 'type':'duration_min', 'filter_type': 'range', 'data': [aggregations['duration__min'],aggregations['duration__max']]},

            {'title': 'Свободные места', 'type':'vacants_number', 'data': aggregations['vacants_number__max']},
            {'title': 'Рейтинг', 'type':'rating', 'data': aggregations['tour_basic__rating__max']},
            {'title': 'Сложность', 'type':'difficulty_level', 'data': aggregations['difficulty_level__max']},
            {'title': 'Комфорт', 'type':'comfort_level', 'data': aggregations['comfort_level__max']}
        ]
        if len(request.query_params):
            filter_data = [filter_data_element for filter_data_element in filter_data if filter_data_element['type'] != list(request.query_params)[-1]]   
        return filter_data