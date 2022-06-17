from orders.serializers import TravelerSerializer
from tours.models import Tour
from utils.prices import get_tour_discounted_price
from django.db.models import F, Q
import math
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from rest_framework.serializers import ValidationError
from orders.models import Order, Traveler


class OrderMixin():
    def perform_book(self, request, *args, **kwargs):
        order, data = self.update_order(request, *args, **kwargs)
        self.check_form_fields(data, order)
        order.status = 'prepayment'
        order.save()
        if order.tour.instant_booking:
            Tour.objects.filter(pk=order.tour_id).update(vacants_number=F('vacants_number')-order.travelers_number)
        return order

    def perform_remove(self, request, *args, **kwargs):
        order = self.get_object()
        Tour.objects.filter(pk=order.tour_id).update(vacants_number=F('vacants_number')+order.travelers_number)
        order.delete()

    def perform_aprove(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = 'pending_prepayment'
        order.save()  
        return order
    
    def perform_decline(self, request, *args, **kwargs):
        order = self.get_object()
        Tour.objects.filter(pk=order.tour_id).update(vacants_number=F('vacants_number')+order.travelers_number)
        order.status = 'declined'
        order.save()
        return order

    def perform_cancel(self, request, *args, **kwargs):
        order = self.get_object()
        Tour.objects.filter(pk=order.tour_id).update(vacants_number=F('vacants_number')+order.travelers_number)
        if hasattr(request.user, 'expert'):
            order.status = 'cancelled_by_expert'
        if hasattr(request.user, 'customer'):
            order.status = 'cancelled_by_customer'
        order.save()
        return order
    
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