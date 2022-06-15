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


class OrderSerializer(serializers.ModelSerializer):
    travelers = TravelerSerializer(many=True, read_only=True)
    members_number = serializers.IntegerField(read_only=True, source='tour.members_number')
    vacants_number = serializers.IntegerField(read_only=True, source='tour.vacants_number') 
    instant_booking = serializers.BooleanField(read_only=True, source='tour.instant_booking')
    tour_dates = TourDatesSerializer(many=True, read_only=True)
    expert = ExpertShortSerializer(many=False, read_only=True, required=False)
    customer = CustomerShortSerializer(many=False, read_only=True, required=False)
    
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'name':{'read_only': True, 'required': False},
            'tour':{'required': False},
            'start_date':{'read_only': True, 'required': False},
            'finish_date':{'read_only': True, 'required': False},
            'price':{'read_only': True, 'required': False},
            'travelers_number':{'required': False},
            'cost':{'read_only': True, 'required': False},
            'postpay_final_date':{'read_only': True, 'required': False},
            'status':{'required': False},
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


