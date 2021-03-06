from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
import threading
from django.core.mail import send_mail
from django.db.models import F, Q, Case, When
from datetime import timedelta, datetime
from django.utils.translation import gettext_lazy as _
from orders.filters import OrderFilter
from orders.mixins import OrderMixin
from django.db.models.query import Prefetch

from orders.models import Order, Traveler
from orders.paginations import OrderResultsSetPagination
from orders.permissions import OrderPermission
from orders.serializers import OrderForExpertSerializer, OrderListSerializer, OrderSerializer
from tours.models import Tour


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet, OrderMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]
    # pagination_class = OrderResultsSetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at', 'start_date']
    ordering = ['-start_date']
    filterset_class = OrderFilter

    def get_queryset(self):
        qs = Order.objects.all()
        if hasattr(self.request.user, 'customer'):
            return qs.filter(customer_id=self.request.user.id)
        if hasattr(self.request.user, 'expert'):
            return qs.filter(expert_id=self.request.user.id).exclude(status__in=['new'])
        if self.request.user.is_staff:
            return qs
    
    def get_serializer_class(self):
        if self.action in ['list', 'book_from_list', 'remove_from_list', 'aprove_from_list', 'decline_from_list', 'cancel_from_list']:
            return OrderListSerializer
        if hasattr(self.request.user, 'expert'):
            return OrderForExpertSerializer
        return super().get_serializer_class()
    

    def create(self, request, *args, **kwargs):
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        tour = Tour.objects.filter(pk=data['tour'].id).annotate(
                discounted_price = Case(
                    When(Q(discount__isnull=True) or Q(discount=0), then=F('price')),
                    When(~Q(discount__isnull=True) and ~Q(discount_starts__isnull=True) and Q(discount__gt=0) and Q(discount_starts__gte=datetime.today()) and Q(discount_finish__gte=datetime.today()) and Q(discount_in_prc=True), then=F('price') - F('price')*F('discount')/100),
                    When(~Q(discount__isnull=True) and Q(discount__gt=0) and Q(discount_starts__lte=datetime.today()) and Q(discount_finish__gte=datetime.today()) and Q(discount_in_prc=False), then=F('price') - F('discount')),
                )
            ).first()
        initial_params = self.get_initial_params(tour)
        costs = self.get_costs(data['travelers_number'], **initial_params)
        order = Order.objects.create(email=request.user.email, tour=data['tour'], travelers_number=data['travelers_number'], customer_id=request.user.id, **initial_params, **costs)
        travelers = []
        for i in range(order.travelers_number):
            travelers.append(Traveler(order=order, index_number=i+1))
        Traveler.objects.bulk_create(travelers)
        order.refresh_from_db()
        order.tour_dates = self.get_tour_dates(order.tour)
        return Response(self.get_serializer(order).data, status=201)
    
    def update(self, request, *args, **kwargs):
        order, data = self.update_order(request, *args, **kwargs)
        order.refresh_from_db()
        order.tour_dates = self.get_tour_dates(order.tour)
        return Response(self.get_serializer(order).data, status=200)
    
    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        order.tour_dates = self.get_tour_dates(order.tour)
        return Response(self.get_serializer(order).data, status=200)
    
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
        order = self.perform_book(request, *args, **kwargs)
        return Response({'redirect_url':f'https://traveler.market/account/orders/{order.id}/success'}, status=200)
    
    @action(['patch'], detail=True)
    def book_from_list(self, request, *args, **kwargs): 
        order = self.perform_book(request, checked=None, *args, **kwargs)
        return Response(self.get_serializer(order).data, status=200)
    
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
        return Response(self.get_serializer(order).data, status=200)
    
    @action(['patch'], detail=True)
    def aprove(self, request, *args, **kwargs):
        self.perform_aprove(request, *args, **kwargs)
        return Response({'redirect_url':'https://traveler.market/account/orders'}, status=200)
    
    @action(['patch'], detail=True)
    def decline_from_list(self, request, *args, **kwargs):
        order = self.perform_decline(request, *args, **kwargs)
        return Response(self.get_serializer(order).data, status=200)
    
    @action(['patch'], detail=True)
    def decline(self, request, *args, **kwargs):
        self.perform_decline(request, *args, **kwargs)
        return Response({'redirect_url':'https://traveler.market/account/orders'}, status=200)

    @action(['patch'], detail=True)
    def cancel_from_list(self, request, *args, **kwargs):
        order = self.perform_cancel(request, *args, **kwargs)
        return Response(self.get_serializer(order).data, status=200)
    
    @action(['patch'], detail=True)
    def cancel(self, request, *args, **kwargs):
        self.perform_cancel(request, *args, **kwargs)
        return Response({'redirect_url':'https://traveler.market/account/orders'}, status=200)
    
    @action(['get'], detail=False)
    def status_list(self, request, *args, **kwargs):
        if hasattr(self.request.user, 'customer') or request.user.is_staff:
            return Response([{'status':choice[0], 'title':choice[1]} for choice in Order.OrderStatus.choices], status=200)
        if hasattr(self.request.user, 'expert'):
            return Response([{'status':choice[0], 'title':choice[1]} for choice in Order.OrderStatus.choices if choice[0] not in ['new']], status=200)
