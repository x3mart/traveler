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
        return obj.tours.filter(Q(tours__tours__booking_delay__lte=F('tours__tours__start_date') - datetime.today().date() - F('tours__tours__postpay_days_before_start'))).first().name