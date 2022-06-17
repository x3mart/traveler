from rest_framework import serializers

from .models import Order, Traveler
from accounts.models import Expert, Customer


class TravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traveler
        exclude = ('order', 'id')


class TourDatesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    tour_date = serializers.SerializerMethodField()

    def get_tour_date(self, obj):
        return f"{obj.start_date.strftime('%d.%m.%Y')} - {obj.finish_date.strftime('%d.%m.%Y')}"

class ExpertShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = ('full_name', 'id')


class CustomerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('full_name', 'id')


class DateWithVerboseMonthAndWeekday(serializers.Field):
    def to_representation(self, value):
        return value.strftime('%d %B %Y (%A)')

class DateWithVerboseMonth(serializers.Field):
    def to_representation(self, value):
        return value.strftime('%d %B %Y')

class OrderSerializer(serializers.ModelSerializer):
    travelers = TravelerSerializer(many=True, read_only=True)
    members_number = serializers.IntegerField(read_only=True, source='tour.members_number')
    vacants_number = serializers.IntegerField(read_only=True, source='tour.vacants_number') 
    instant_booking = serializers.BooleanField(read_only=True, source='tour.instant_booking')
    tour_dates = TourDatesSerializer(many=True, read_only=True)
    expert = ExpertShortSerializer(many=False, read_only=True, required=False)
    customer = CustomerShortSerializer(many=False, read_only=True, required=False)
    start_date = DateWithVerboseMonthAndWeekday(read_only=True)
    finish_date = DateWithVerboseMonthAndWeekday(read_only=True)
    postpay_final_date = DateWithVerboseMonth(read_only=True)
    actions = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Order
        exclude = ()
        extra_kwargs = {
            'name':{'read_only': True, 'required': False},
            'tour':{'required': False},
            'price':{'read_only': True, 'required': False},
            'travelers_number':{'required': False},
            'cost':{'read_only': True, 'required': False},
            'status':{'read_only': True, 'required': False},
            'difficulty_level':{'read_only': True, 'required': False},
            'comfort_level':{'read_only': True, 'required': False},
            'tour_excluded_services':{'read_only': True, 'required': False},
            'tour_included_services':{'read_only': True, 'required': False},
            'created_at':{'read_only': True, 'required': False},
            'currency':{'read_only': True, 'required': False},
            'book_price':{'read_only': True, 'required': False},
            'postpay':{'read_only': True, 'required': False},
            'book_cost':{'read_only': True, 'required': False},
            'full_postpay':{'read_only': True, 'required': False},
            'languages':{'read_only': True, 'required': False},
            'duration':{'read_only': True, 'required': False}
        }
    
    def get_actions(self, order):
        user = self.context['request'].user
        if hasattr(user, 'expert'):
            return self.get_actions_for_expert(order)
        if hasattr(user, 'customer'):
            return self.get_actions_for_customer(order)
    
    def get_actions_for_customer(self, order):
        if order.status == 'new' and not order.tour.instant_booking:
            return [{'action':'ask_confirmation/', 'title': 'Хочу поехать!', 'color':'button-success', 'confirmation':False}]
        if order.status == 'new' and order.tour.instant_booking:
            return [{'action':'book/', 'title': 'Забронировать', 'color':'button-success', 'confirmation':False}]
        if order.status == 'pending_confirmation':
            return [{'action':'remove/', 'title': 'Удалить', 'color':'button-danger', 'confirmation':True}]
        if order.status == 'pending_prepayment':
            return [{'action': 'book/', 'title': 'Забронировать', 'color':'button-success', 'confirmation':False}, {'action':'cancel/', 'title': 'Отменить', 'color':'button-danger', 'confirmation':True}]
        if order.status == 'prepayment':
            return [{'action': 'fullpayment/', 'title': 'Оплатить все', 'color':'button-success', 'confirmation':False}]
        return None
        
    
    def get_actions_for_expert(self, order):
        if order.status == 'pending_confirmation':
            return [{'action': 'aprove/', 'title': 'Подтвердить', 'color':'button-success', 'confirmation':False}, {'action':'decline/', 'title': 'Отказать', 'color':'button-danger', 'confirmation':True}]
        return None
    
class OrderForExpertSerializer(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        exclude = ('phone', 'email')

class OrderListSerializer(serializers.ModelSerializer):
    expert = ExpertShortSerializer(many=False, read_only=True, required=False)
    customer = CustomerShortSerializer(many=False, read_only=True, required=False)
    start_date = DateWithVerboseMonth(read_only=True)
    finish_date = DateWithVerboseMonth(read_only=True)
    postpay_final_date = DateWithVerboseMonth(read_only=True)
    status = serializers.CharField(read_only=True, source='get_status_display')
    travelers = travelers = TravelerSerializer(many=True, read_only=True)
    actions = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'expert', 'customer', 'start_date', 'finish_date', 'postpay_final_date', 'status', 'name', 'travelers_number', 'currency', 'cost', 'book_cost', 'book_price', 'travelers', 'actions')

    def get_actions(self, order):
        user = self.context['request'].user
        if hasattr(user, 'expert'):
            return self.get_list_actions_for_expert(order)
        if hasattr(user, 'customer'):
            return self.get_list_actions_for_customer(order)

    def get_list_actions_for_customer(self, order):
        if order.status == 'new':
            return [{'action':'remove_from_list/', 'title': 'Удалить', 'color':'#404040', 'confirmation':True}]
        if order.status == 'pending_confirmation':
            return [{'action':'remove_from_list/', 'title': 'Удалить', 'color':'#404040', 'confirmation':True}]
        if order.status == 'pending_prepayment':
            return [{'action': 'book_from_list/', 'title': 'Забронировать', 'color':'#2aa2d6', 'confirmation':False}, {'action':'cancel_from_list/', 'title': 'Отменить', 'color':'#404040', 'confirmation':True}]
        if order.status == 'prepayment':
            return [{'action': 'fullpayment_from_list/', 'title': 'Оплатить все', 'color':'#2aa2d6', 'confirmation':False}, {'action':'cancel_from_list/', 'title': 'Отменить', 'color':'#404040', 'confirmation':True}]
        return None
        
    def get_list_actions_for_expert(self, order):
        if order.status == 'pending_confirmation':
            return [{'action': 'aprove_from_list/', 'title': 'Подтвердить', 'color':'#2aa2d6', 'confirmation':False}, {'action':'decline_from_list/', 'title': 'Отказать', 'color':'#404040', 'confirmation':True}]
        return None
