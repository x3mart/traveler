from rest_framework import serializers
from .models import TourReview

class TourReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourReview
        fields = '__all__'