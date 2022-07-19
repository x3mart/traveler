from rest_framework import serializers
from accounts.serializers import CustomerSerializer
from orders.serializers import CustomerShortSerializer

from tours.serializers import TourListSerializer
from .models import TourReview

class TourReviewSerializer(serializers.ModelSerializer):
    tour = TourListSerializer(many=False, read_only=True)
    author = CustomerShortSerializer(many=False, read_only=True)
    class Meta:
        model = TourReview
        fields = '__all__'