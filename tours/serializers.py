from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import TourBasic


class TourBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = TourBasic
        fields = '__all__'

class TourBasicListSerializer(serializers.ModelSerializer):
    expert_first_name = serializers.CharField(source='expert.first_name')
    expert_last_name = serializers.CharField(source='expert.last_name')
    expert_rating = serializers.DecimalField(max_digits=2, decimal_places=1, source='expert.rating')
    start_country = serializers.CharField(source='start_country.name')

    class Meta:
        model = TourBasic
        fields = ['name', 'start_country', 'expert_first_name', 'expert_last_name', 'expert_rating']
