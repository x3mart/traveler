from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
import threading
from django.core.mail import send_mail
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from orders.filters import OrderFilter
from orders.mixins import OrderMixin

from orders.models import Order, Traveler
from orders.permissions import OrderPermission
from orders.serializers import OrderForExpertSerializer, OrderListSerializer, OrderSerializer
from tours.models import Tour


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet, OrderMixin):
    queryset = Order.objects.prefetch_related('tour', 'expert', 'customer', 'travelers')
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at', 'id', 'status']
    ordering = ['-start_date']
    filterset_class = OrderFilter

    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.request.user, 'customer'):
            return qs.filter(customer_id=self.request.user.id)
        if hasattr(self.request.user, 'expert'):
            return qs.filter(expert_id=self.request.user.id).exclude(status__in=['new'])
        if self.request.user.is_staff:
            return qs
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        if hasattr(self.request.user, 'expert'):
            return OrderForExpertSerializer
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
        return Response(self.get_serializer(data=order, many=False).data, status=200)
    
    @action(['patch'], detail=True)
    def ask_confirmation(self, request, *args, **kwargs):
        order, data = self.update_order(request, *args, **kwargs)
        self.check_form_fields(data, order)
        order.status = 'pending_confirmation'
        order.save()
        Tour.objects.filter(pk=order.tour_id).update(vacants_number=F('vacants_number')-order.travelers_number)
        return Response({'redirect_url':'https://traveler.market/account/orders'}, status=200)
    
    @action(['patch'], detail=True)
    def book(self, request, *args, **kwargs):
        self.perform_book(request, *args, **kwargs)
        return Response({'redirect_url':'https://www.tinkoff.ru/invest/open-api/'}, status=200)
    
    @action(['patch'], detail=True)
    def book_from_list(self, request, *args, **kwargs):
        order = self.perform_book(request, *args, **kwargs)
        return Response({'redirect_url':'https://www.tinkoff.ru/invest/open-api/'}, status=200)
    
    @action(['patch'], detail=True)
    def remove(self, request, *args, **kwargs):
        self.perform_remove(request, *args, **kwargs)
        return Response({'redirect_url':'https://traveler.market/account/orders'}, status=200)
    
    @action(['patch'], detail=True)
    def remove_from_list(self, request, *args, **kwargs):
        self.perform_remove(request, *args, **kwargs)
        return Response({}, status=204)
        
    @action(['patch'], detail=True)
    def aprove_from_list(self, request, *args, **kwargs):
        order = self.perform_aprove(request, *args, **kwargs)
        return Response(OrderListSerializer(order, many=False, context={'request':request}).data, status=200)
    
    @action(['patch'], detail=True)
    def aprove(self, request, *args, **kwargs):
        self.perform_aprove(request, *args, **kwargs)
        return Response({'redirect_url':'https://traveler.market/account/orders'}, status=200)
    
    @action(['patch'], detail=True)
    def decline_from_list(self, request, *args, **kwargs):
        order = self.perform_decline(request, *args, **kwargs)
        return Response(OrderListSerializer(order, many=False, context={'request':request}).data, status=200)
    
    @action(['patch'], detail=True)
    def decline(self, request, *args, **kwargs):
        self.perform_decline(request, *args, **kwargs)
        return Response({'redirect_url':'https://traveler.market/account/orders'}, status=200)

    @action(['patch'], detail=True)
    def cancel_from_list(self, request, *args, **kwargs):
        order = self.perform_cancel(self, request, *args, **kwargs)
        return Response(OrderListSerializer(order, many=False, context={'request':request}).data, status=200)
    
    @action(['patch'], detail=True)
    def cancel(self, request, *args, **kwargs):
        self.perform_cancel(self, request, *args, **kwargs)
        return Response({'redirect_url':'https://traveler.market/account/orders'}, status=200)
    
