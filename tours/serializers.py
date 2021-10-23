from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import TourBasic


class TourBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = TourBasic
        fields = '__all__'

class TourBasicListSerializer(serializers.ModelSerializer):
    # expert = serializers.CharField(source='expert.full_name')

    class Meta:
        model = TourBasic
        fields = ['name', 'start_country', ]
