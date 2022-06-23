from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import F, Q

from languages.models import Language
from orders.models import Order
from tours.models import TourAccomodation, TourPropertyType

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
            'filter_set': self.statuses
        })
    
    def paginate_queryset(self, queryset, request, view=None):
        self.filters = self.status_list(request)
        return super().paginate_queryset(queryset, request, view)
    
    def status_list(self, queryset,request):
        tour_types = queryset.objects.filter(Q(tours_by_basic_type__in=queryset) | Q(tours_by_additional_types__in=queryset)).order_by('name').values('name', 'id').distinct()      
        languages = Language.objects.filter(tours__in=queryset).order_by('name').values('name', 'id').distinct()
        property_type = TourPropertyType.objects.filter(tours__in=queryset).order_by('name').values('name', 'id').distinct()
        accomodation = TourAccomodation.objects.filter(tours__in=queryset).order_by('name').values('name', 'id').distinct()

        filter_data = [
            {'title': 'Типы туров', 'type':'tour_types', 'data': tour_types},
            {'title': 'Языки тура', 'type':'languages', 'data': languages},
            {'title': 'Проживание', 'type':'property_type', 'data': property_type},
            {'title': 'Размещение', 'type':'accomodation', 'data': accomodation}
        ]
            
        return Response(filter_data, status=200)