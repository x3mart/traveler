from dataclasses import fields
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from accounts.models import Expert
from accounts.serializers import ExpertListSerializer
from .models import Tour, TourDay, TourPropertyImage, TourImage, TourType


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPropertyImage
        exclude = ('tour',)

class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        exclude = ('tour',)


class TourDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDay
        exclude = ('tour',)

class TourTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourType
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    basic_type = serializers.StringRelatedField(many=False,)
    additional_types = serializers.StringRelatedField(many=True,)
    start_region = serializers.StringRelatedField(many=False,)
    finish_region = serializers.StringRelatedField(many=False,)
    start_country = serializers.StringRelatedField(many=False,)
    finish_country = serializers.StringRelatedField(many=False,)
    start_city = serializers.StringRelatedField(many=False,)
    finish_city = serializers.StringRelatedField(many=False,)
    property_types = serializers.StringRelatedField(many=True, source='basic_tour.tour_property_types')
    property_images = PropertyImageSerializer(many=True,)
    tour_images = TourImageSerializer(many=True,)
    languages = serializers.StringRelatedField(many=True,)
    currency = serializers.StringRelatedField(many=False, source='currency.short_name')
    expert = ExpertListSerializer(many=False,)
    tour_days = TourDaySerializer(many=True,)
    tour_impressions = serializers.StringRelatedField(many=True,)
    tour_included_services = serializers.StringRelatedField(many=True,)
    tour_excluded_services = serializers.StringRelatedField(many=True,)

    class Meta:
        model = Tour
        fields = ('id', 'rating', 'reviews_count', 'name', 'wallpaper', 'basic_type', 'additional_types', 'start_region', 'finish_region', 'start_country', 'finish_country', 'start_city', 'finish_city', 'description', 'plan', 'cancellation_terms', 'difficulty_level', 'property_types', 'difficulty_description', 'comfort_level', 'babies_alowed', 'animals_not_exploited', 'property_images', 'start_date', 'finish_date', 'start_time', 'finish_time', 'direct_link', 'instant_booking', 'members_number', 'prepayment', 'postpayment', 'team_member', 'currency', 'price', 'cost', 'discount', 'languages', 'is_guaranteed', 'flight_included', 'scouting', 'tour_images', 'expert', 'tour_days', 'tour_impressions', 'tour_included_services', 'tour_excluded_services',)


class TourListSerializer(serializers.ModelSerializer):
    expert = ExpertListSerializer(many=False, source='basic_tour.expert')
    rating = serializers.DecimalField(decimal_places=1, max_digits=2, source='basic_tour.rating')
    reviews_count = serializers.IntegerField(source='basic_tour.reviews_count')
    name = serializers.CharField(source='basic_tour.name')
    tmb_wallpaper = serializers.ImageField(source='basic_tour.tmb_wallpaper')
    start_country = serializers.StringRelatedField(many=False, source='basic_tour.start_country')
    class Meta:
        model = Tour
        fields = ['id', 'rating', 'reviews_count', 'name', 'tmb_wallpaper', 'start_date', 'finish_date', 'start_country',  'expert', 'price', 'cost', 'discount']

class TourBasicSerializer(serializers.ModelSerializer):
    basic_type = TourTypeSerializer(many=False, required=False)
    additional_types  = TourTypeSerializer(many=True, required=False)
    class Meta:
        model = Tour
        fields ='__all__'
        extra_kwargs = {
            'expert': {'required': False,},
        }
    
    # def create(self, validated_data):
    #     validated_data['expert_id'] = self.context['request'].user.id
    #     validated_data['is_draft'] = True
    #     return super().create(validated_data)
