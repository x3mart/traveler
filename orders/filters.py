from django_filters import rest_framework as filters
from django_filters.filters import MultipleChoiceFilter

from orders.models import Order


class OrderFilter(filters.FilterSet):
    status = MultipleChoiceFilter(choices=Order.OrderStatus)

    class Meta:
        model = Order
        fields = ['status']