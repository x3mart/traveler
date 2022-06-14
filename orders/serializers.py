from rest_framework import serializers

from .models import Order, Traveler


class TravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traveler
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    travelers = TravelerSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'customer':{'read_only': True, 'required': False},
            'expert':{'read_only': True, 'required': False},
            'name':{'read_only': True, 'required': False},
            'tour_id':{'required': False},
            'start_date':{'read_only': True, 'required': False},
            'finish_date':{'read_only': True, 'required': False},
            'price':{'read_only': True, 'required': False},
            'travelers_number':{'required': False},
            'cost':{'read_only': True, 'required': False},
            'postpay_final_date':{'read_only': True, 'required': False},
            'status':{'read_only': True, 'required': False},
            'difficulty_level':{'read_only': True, 'required': False},
            'comfort_level':{'read_only': True, 'required': False},
            'tour_excluded_services':{'read_only': True, 'required': False},
            'tour_included_services':{'read_only': True, 'required': False},
            'created_at':{'read_only': True, 'required': False},
        }


