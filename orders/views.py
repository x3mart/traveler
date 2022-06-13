from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
import threading
from django.core.mail import send_mail
import math

from orders.models import Order
from orders.serializers import OrderSerializer
from tours.models import Tour
from utils.prices import get_tour_discounted_price

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [OrderPermission]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at', 'id', 'status']
    ordering = ['start_date']
    # filterset_class = TourFilter

    def get_queryset(self):
        if self.action == 'new_order':
            return Tour.objects.all()
        return super().get_queryset()
    

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

    @action(['get'], detail=True)
    def new_order(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        travelers_number = data.get('travelers_number')
        tour = self.get_object()
        tour.tour_id = tour.id
        tour.id = None
        tour.customer = request.user
        tour.expert = tour.tour_basic.expert
        tour.tour_name = tour.name
        tour.tour_price = get_tour_discounted_price(tour) if get_tour_discounted_price(tour) else tour.price
        tour.tour_cost = tour.price*travelers_number
        tour.prepay_amount = math.ceil(tour.cost*tour.prepay_amount/100)*travelers_number if tour.prepay_in_prc else tour.prepay_amount*travelers_number
        tour.postpay = tour.cost - tour.prepay_amount
        return Response(OrderSerializer(tour, many=False, context={'request':request}).data, status=200)