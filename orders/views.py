from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.http import HttpResponseRedirect
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
import threading
from django.core.mail import send_mail
import math
from datetime import datetime
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

from orders.models import Order, Traveler
from orders.permissions import OrderPermission
from orders.serializers import OrderListSerializer, OrderSerializer, TravelerSerializer
from tours.models import Tour
from utils.prices import get_tour_discounted_price

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('tour', 'expert', 'customer', 'travelers')
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at', 'id', 'status']
    ordering = ['-start_date']
    # filterset_class = TourFilter

    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.request.user, 'customer'):
            return qs.filter(customer_id=self.request.user.id)
        if hasattr(self.request.user, 'expert'):
            return qs.filter(expert_id=self.request.user.id)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return super().get_serializer_class()
    

    def create(self, request, *args, **kwargs):
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        initial_params = self.get_initial_params(data['tour'])
        costs = self.get_costs(data['travelers_number'], **initial_params)
        order = Order.objects.create(email=request.user.email, tour=data['tour'], travelers_number=data['travelers_number'], customer_id=request.user.id, **initial_params, **costs)
        travelers = []
        for i in range(order.travelers_number):
            travelers.append(Traveler(order=order, index_number=i+1))
        Traveler.objects.bulk_create(travelers)
        order.refresh_from_db()
        order.tour_dates = self.get_tour_dates(order.tour)
        return Response(OrderSerializer(order, many=False, context={'request':request}).data, status=201)
    
    def update(self, request, *args, **kwargs):
        order, data = self.update_order(request, *args, **kwargs)
        order.refresh_from_db()
        order.tour_dates = self.get_tour_dates(order.tour)
        return Response(OrderSerializer(order, many=False, context={'request':request}).data, status=200)
    
    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        order.tour_dates = self.get_tour_dates(order.tour)
        return Response(OrderSerializer(order, many=False, context={'request':request}).data, status=200)
    
    @action(['post'], detail=True)
    def ask_confirmation(self, request, *args, **kwargs):
        order, data = self.update_order(request, *args, **kwargs)
        self.check_form_fields(data, order)
        order.status = 'pending_confirmation'
        order.save()
        Tour.objects.filter(pk=order.tour_id).update(vacants_number=F('vacants_number')-order.travelers_number)
        return HttpResponseRedirect(redirect_to='https://www.tinkoff.ru/invest/open-api/')
        # return Response(OrderListSerializer(orders, many=True, context={'request':request}).data, status=200)
    
    def perform_book(self, request, *args, **kwargs):
        order, data = self.update_order(request, *args, **kwargs)
        self.check_form_fields(data, order)
        order.status = 'prepayment'
        order.save()
        if order.tour.instant_booking:
            Tour.objects.filter(pk=order.tour_id).update(vacants_number=F('vacants_number')-order.travelers_number)
    
    @action(['post'], detail=True)
    def book(self, request, *args, **kwargs):
        self.perform_book(request, *args, **kwargs)
        return HttpResponseRedirect('https://traveler.market/account/orders')
    
    @action(['post'], detail=True)
    def book_from_list(self, request, *args, **kwargs):
        self.perform_book(request, *args, **kwargs)
        orders =  self.get_queryset()
        return Response(OrderListSerializer(orders, many=True, context={'request':request}).data, status=200)
    
    def perform_remove(self, request, *args, **kwargs):
        order = self.get_object()
        Tour.objects.filter(pk=order.tour_id).update(vacants_number=F('vacants_number')+order.travelers_number)
        order.delete()

    @action(['post'], detail=True)
    def remove_from_list(self, request, *args, **kwargs):
        self.perform_remove(request, *args, **kwargs)
        orders =  self.get_queryset()
        return Response(OrderListSerializer(orders, many=True, context={'request':request}).data, status=200)
    
    @action(['post'], detail=True)
    def remove(self, request, *args, **kwargs):
        self.perform_remove(request, *args, **kwargs)
        return HttpResponseRedirect(redirect_to='https://traveler.market/account/orders')
        
    def perform_aprove(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = 'pending_prepayment'
        order.save()  
    
    @action(['post'], detail=True)
    def aprove_from_list(self, request, *args, **kwargs):
        self.perform_aprove(request, *args, **kwargs)
        orders =  self.get_queryset()
        return Response(OrderListSerializer(orders, many=True, context={'request':request}).data, status=200)
    
    @action(['post'], detail=True)
    def aprove(self, request, *args, **kwargs):
        self.perform_aprove(request, *args, **kwargs)
        return HttpResponseRedirect(redirect_to='https://traveler.market/account/orders')
    
    def perform_decline(self, request, *args, **kwargs):
        order = self.get_object()
        Tour.objects.filter(pk=order.tour_id).update(vacants_number=F('vacants_number')+order.travelers_number)
        order.status = 'declined'
        order.save()
    
    @action(['post'], detail=True)
    def decline_from_list(self, request, *args, **kwargs):
        self.perform_decline(request, *args, **kwargs)
        orders =  self.get_queryset()
        return Response(OrderListSerializer(orders, many=True, context={'request':request}).data, status=200)
    
    @action(['post'], detail=True)
    def decline(self, request, *args, **kwargs):
        self.perform_decline(request, *args, **kwargs)
        return HttpResponseRedirect(redirect_to='https://traveler.market/account/orders')
    
    def perform_cancel(self, request, *args, **kwargs):
        order = self.get_object()
        Tour.objects.filter(pk=order.tour_id).update(vacants_number=F('vacants_number')+order.travelers_number)
        if hasattr(request.user, 'expert'):
            order.status = 'cancelled_by_expert'
        if hasattr(request.user, 'customer'):
            order.status = 'cancelled_by_customer'
        order.save()

    @action(['post'], detail=True)
    def cancel_from_list(self, request, *args, **kwargs):
        self.perform_cancel(self, request, *args, **kwargs)
        orders =  self.get_queryset()
        return Response(OrderListSerializer(orders, many=True, context={'request':request}).data, status=200)
    
    @action(['post'], detail=True)
    def cancel(self, request, *args, **kwargs):
        self.perform_cancel(self, request, *args, **kwargs)
        return HttpResponseRedirect(redirect_to='https://traveler.market/account/orders')
    
    def update_order(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(data=request.data)
        travelers = request.data.get('travelers')
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        data['travelers_number'] = len(travelers)
        if not data['travelers_number']:
            data['travelers_number'] = order.travelers_number
        initial_params = self.get_initial_params(data['tour'])
        costs = self.get_costs(data['travelers_number'], order.price, order.book_price, order.postpay)
        order.travelers.all().delete()
        for traveler in travelers:
            traveler_serializer = TravelerSerializer(data=traveler)
            if traveler_serializer.is_valid(raise_exception=True):
                Traveler.objects.create(order=order, **traveler_serializer.validated_data)
        Order.objects.filter(pk=order.id).update(**data, **costs, **initial_params)

        return order, data
    def get_initial_params(self, tour):
        return {
            'currency':tour.currency.sign,
            'expert': tour.tour_basic.expert,
            'name': tour.name,
            'difficulty_level': tour.difficulty_level,
            'comfort_level': tour.comfort_level,
            'tour_excluded_services': tour.tour_excluded_services,
            'tour_included_services': tour.tour_included_services,
            'languages': list(tour.languages.all().values_list('name', flat=True)),
            'start_date': tour.start_date,
            'finish_date': tour.finish_date,
            'duration': tour.duration,
            'postpay_final_date': (tour.start_date - tour.postpay_days_before_start),
            'price': get_tour_discounted_price(tour) if get_tour_discounted_price(tour) else tour.price,
            'book_price': math.ceil(tour.price*tour.prepay_amount/100) if tour.prepay_in_prc else tour.prepay_amount,
            'postpay': tour.price - math.ceil(tour.price*tour.prepay_amount/100) if tour.prepay_in_prc else tour.price - tour.prepay_amount
        }
    
    def get_costs(self, travelers_number, price, book_price, postpay, **kwargs):
        return {
            'cost': price*travelers_number,
            'book_cost': book_price*travelers_number,
            'full_postpay': postpay*travelers_number
        }
    
    def get_tour_dates(self, tour):
        return Tour.objects.filter(tour_basic_id=tour.tour_basic.id).filter(is_active=True).filter(direct_link=False).filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start'))).only('id', 'start_date', 'finish_date')

    def check_form_fields(self, data, order):
        errors={}
        travelers_errors = []
        if not data.get('email'):
            errors.update({'email': [_('Обязательное поле')]})
        if not data.get('phone'):
            errors.update({'phone': [_('Обязательное поле')]})
        travelers = order.travelers.all()
        for traveler in travelers:
            traveler_errors = self.check_traveler_fields(traveler)
            if traveler_errors:
                travelers_errors.append({'index_number':traveler.index_number, 'errors':traveler_errors})
        if travelers_errors:
            errors.update({'travelers':travelers_errors})
        if errors:
            raise ValidationError(errors)
        return None
    
    def check_traveler_fields(self, traveler):
        traveler_errors = {}
        fields = [field.name for field in Traveler._meta.get_fields()]
        for field in fields:
            if not getattr(traveler, field):
                traveler_errors.update({field:[_('Обязательное поле')]})
        return traveler_errors
    
    # def get_status(self, data, order):
    #     errors = {}
    #     if data['status'] == 'form_completed':
    #         errors.update(self.check_form_fields(data, order, errors))
    #     if errors:
    #         raise ValidationError(errors)
    #     return data['status']
    
    
