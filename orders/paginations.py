from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from orders.models import Order

class OrderResultsSetPagination(PageNumberPagination):
    page_size = 50
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
            'status_list': self.status_list()
        })
    
    def paginate_queryset(self, queryset, request, view=None):
        page = super().paginate_queryset(queryset, request, view)
        print(page)
        return page
    
    def status_list(self):
        if hasattr(self.request.user, 'customer') or self.request.user.is_staff:
            return [{'status':choice[0], 'title':choice[1]} for choice in Order.OrderStatus.choices]
        if hasattr(self.request.user, 'expert'):
            return [{'status':choice[0], 'title':choice[1]} for choice in Order.OrderStatus.choices if choice[0] not in ['new']]