from rest_framework import serializers
from accounts.serializers import CustomerSerializer
from orders.serializers import CustomerShortSerializer

from tours.serializers import TourListSerializer
from datetime import datetime
from django.db.models import Q, F
from .models import TourReview

class TourReviewSerializer(serializers.ModelSerializer):
    tour = serializers.SerializerMethodField(read_only=True)
    author = CustomerShortSerializer(many=False, read_only=True)
    class Meta:
        model = TourReview
        fields = '__all__'
    
    def get_tour(self, obj):
        return obj.tour.tours.filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start'))).first().name