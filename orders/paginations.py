from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from orders.models import Order

class OrderResultsSetPagination(PageNumberPagination):
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
            'orders_number': self.orders_number,
            'status_list': self.statuses
        })
    
    def paginate_queryset(self, queryset, request, view=None):
        # print(self)
        self.statuses = self.status_list(request)
        self.orders_number = queryset.count()
        return super().paginate_queryset(queryset, request, view)
    
    def status_list(self, request):
        # print(self)
        if hasattr(request.user, 'customer') or self.request.user.is_staff:
            return [{'status':choice[0], 'title':choice[1]} for choice in Order.OrderStatus.choices]
        if hasattr(request.user, 'expert'):
            return [{'status':choice[0], 'title':choice[1]} for choice in Order.OrderStatus.choices if choice[0] not in ['new']]