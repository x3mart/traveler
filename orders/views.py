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
from datetime import datetime
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

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
    ordering = ['-start_date']
    # filterset_class = TourFilter

    def get_queryset(self):
        return super().get_queryset()
    

    def create(self, request, *args, **kwargs):
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        initial_params = self.get_initial_params(data['tour'])
        costs = self.get_costs(data['travelers_number'], **initial_params)
        order = Order.objects.create(tour=data['tour'], travelers_number=data['travelers_number'], customer_id=request.user.id, **initial_params, **costs)
        travelers = []
        for i in range(order.travelers_nuber):
            travelers.append(Traveler(order=order))
        Traveler.objects.bulk_create(travelers)
        order.refresh_from_db()
        order.tour_dates = self.get_tour_dates(order.tour)
        return Response(OrderSerializer(order, many=False, context={'request':request}).data, status=201)
    
    def update(self, request, *args, **kwargs):
        errors = {'field':[_('Какая то ошибка')]}
        serializer =self.get_serializer(data=request.data)
        travelers = request.data.get('travelers')
        # if not serializer.is_valid():
        #     print(serializer.validated_data)
        #     errors.update(serializer.validated_data)
        #     raise ValidationError(errors)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        # if not travelers:
        #     raise ValidationError({'travelers': [_('Заполните данные о Путешественниках')]})
        # if not data.get('phone'):
        #     raise ValidationError({'phone': [_('Обязательное поле')]})
        order = self.get_object()
        costs = self.get_costs(data['travelers_number'], order.price, order.book_price, order.postpay)
        Order.objects.filter(pk=order.id).update(**data, **costs)
        order.travelers.all().delete()
        for traveler in travelers:
            traveler_serializer = TravelerSerializer(data=traveler)
            if traveler_serializer.is_valid():
                Traveler.objects.create(order=order, **traveler_serializer.validated_data)
        order.refresh_from_db()
        order.tour_dates = self.get_tour_dates(order.tour)
        return Response(OrderSerializer(order, many=False, context={'request':request}).data, status=200)
    
    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        order.tour_dates = self.get_tour_dates(order.tour)
        return Response(OrderSerializer(order, many=False, context={'request':request}).data, status=200)
    

    def get_initial_params(self, tour):
        locale.setlocale(locale.LC_ALL, "ru_RU.utf8")
        return {
            'tour_id':tour.id,
            'expert': tour.tour_basic.expert,
            'name': tour.name,
            'difficulty_level': tour.difficulty_level,
            'comfort_level': tour.comfort_level,
            'tour_excluded_services': tour.tour_excluded_services,
            'tour_included_services': tour.tour_included_services,
            'languages': list(tour.languages.all().values_list('name', flat=True)),
            'start_date': tour.start_date.strftime('%d %B %Y (%A)'),
            'finish_date': tour.finish_date.strftime('%d %B %Y (%A)'),
            'duration': tour.duration,
            'postpay_final_date': (tour.start_date - tour.postpay_days_before_start).strftime('%d %B %Y'),
            'price': get_tour_discounted_price(tour) if get_tour_discounted_price(tour) else tour.price,
            'book_price': math.ceil(tour.price*tour.prepay_amount/100) if tour.prepay_in_prc else tour.prepay_amount,
            'postpay': tour.price - tour.prepay_amount
        }
    
    def get_costs(self, travelers_number, price, book_price, postpay, **kwargs):
        return {
            'cost': price*travelers_number,
            'book_cost': book_price*travelers_number,
            'full_postpay': postpay*travelers_number
        }
    
    def get_tour_dates(self, tour):
        return Tour.objects.filter(tour_basic_id=tour.tour_basic.id).filter(is_active=True).filter(direct_link=False).filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start'))).only('id', 'start_date', 'finish_date')
