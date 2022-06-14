from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
import threading
from django.core.mail import send_mail
import math
import locale

from orders.models import Order, Traveler
from orders.serializers import OrderSerializer, TravelerSerializer
from tours.models import Tour
from utils.prices import get_tour_discounted_price

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [OrderPermission]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at', 'id', 'status']
    ordering = ['tour_start_date']
    # filterset_class = TourFilter

    def get_queryset(self):
        return super().get_queryset()
    

    def create(self, request, *args, **kwargs):
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        initial_params = self.get_initional_params(data['tour_id'])
        costs = self.get_costs(data['travelers_number'], **initial_params)
        order = Order.objects.create(travelers_number=data['travelers_number'], customer_id=request.user.id, **initial_params, **costs)
        return Response(OrderSerializer(order, many=False, context={'request':request}).data, status=201)
    
    def update(self, request, *args, **kwargs):
        errors = []
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            data = serializer.validated_data
        else:
            errors.append(serializer.errors)
        for traveler in travelers:
            traveler_serializer = TravelerSerializer(data=traveler)
            if not serializer.is_valid():
                errors.append(serializer.errors)
        if errors.exists():
            return Response(errors, status=400)
        order = self.get_object()
        costs = self.get_costs(data['travelers_number'], order.tour_price, order.book_price, order.postpay)
        Order.objects.filter(pk=order.id).update(**data, **costs)
        travelers = request.data.get('travelers')
        order.travelers.delete()
        for traveler in travelers:
            traveler_serializer = TravelerSerializer(data=traveler)
            if serializer.is_valid():
                Traveler.objects.create(order=order, **traveler_serializer.validated_data)
        order.refresh_from_db()
        return Response(OrderSerializer(order, many=False, context={'request':request}).data, status=200)
    

    def get_initional_params(self, tour_id):
        locale.setlocale(locale.LC_ALL, "ru")
        tour = Tour.objects.get(pk=tour_id)
        return {
            'tour_id':tour_id,
            'expert': tour.tour_basic.expert,
            'tour_name': tour.name,
            'tour_start_date': tour.start_date.strftime('%d %B %Y'),
            'tour_finish_date': tour.finish_date.strftime('%d %B %Y'),
            'postpay_final_date': (tour.start_date - tour.postpay_days_before_start).strftime('%d %B %Y'),
            'tour_price': get_tour_discounted_price(tour) if get_tour_discounted_price(tour) else tour.price,
            'book_price': math.ceil(tour.price*tour.prepay_amount/100) if tour.prepay_in_prc else tour.prepay_amount,
            'postpay': tour.price - tour.prepay_amount
        }
    
    def get_costs(self, travelers_number, tour_price, book_price, postpay, **kwargs):
        return {
            'tour_cost': tour_price*travelers_number,
            'book_cost': book_price*travelers_number,
            'full_postpay': postpay*travelers_number
        }
