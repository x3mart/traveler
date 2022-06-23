from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import F, Q, Max, Min

from languages.models import Language
from orders.models import Order
from tours.models import TourAccomodation, TourPropertyType, TourType

class TourResultsSetPagination(PageNumberPagination):
    page_size = 3
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
        aggregations = queryset.aggregate(Min('discounted_price'), Max('discounted_price'), Min('age_starts'), Max('age_ends'))

        filter_data = [
            {'title': 'Типы туров', 'type':'tour_types', 'data': tour_types},
            {'title': 'Языки тура', 'type':'languages', 'data': languages},
            {'title': 'Проживание', 'type':'property_type', 'data': property_type},
            {'title': 'Размещение', 'type':'accomodation', 'data': accomodation},
            {'title': 'Цена от', 'type':'price_min', 'data': aggregations['discounted_price__min']},
            {'title': 'Цена до', 'type':'price_max', 'data': aggregations['discounted_price__max']},
            {'title': 'Возраст от', 'type':'age_starts', 'data': aggregations['age_starts__min']},
            {'title': 'Возраст до', 'type':'price_max', 'data': aggregations['age_ends__max']},
        ]
            
        return filter_data