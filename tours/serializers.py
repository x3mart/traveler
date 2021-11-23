from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from utils.translate import TranslatedModelSerializer
from .models import TourAdvanced, TourBasic, TourPropertyImage, TourType


class PropertyImageSerializer(TranslatedModelSerializer):
    class Meta:
        model = TourPropertyImage
        exclude = ('tour',)


class TourSerializer(TranslatedModelSerializer):
    rating = serializers.DecimalField(decimal_places=1, max_digits=2, source='basic_tour.rating')
    name = serializers.CharField(source='basic_tour.name')
    wallpaper = serializers.ImageField(source='basic_tour.wallpaper')
    basic_type = serializers.StringRelatedField(many=False, source='basic_tour.basic_type')
    additional_types = serializers.StringRelatedField(many=True, source='basic_tour.additional_types')
    start_region = serializers.StringRelatedField(many=False, source='basic_tour.start_region')
    finish_region = serializers.StringRelatedField(many=False, source='basic_tour.finish_region')
    start_country = serializers.StringRelatedField(many=False, source='basic_tour.start_country')
    finish_country = serializers.StringRelatedField(many=False, source='basic_tour.finish_country')
    start_city = serializers.StringRelatedField(many=False, source='basic_tour.start_city')
    finish_city = serializers.StringRelatedField(many=False, source='basic_tour.finish_city')
    description = serializers.CharField(source='basic_tour.description')
    plan = serializers.CharField(source='basic_tour.plan')
    cancellation_terms = serializers.CharField(source='basic_tour.cancellation_terms')
    difficulty_level = serializers.IntegerField(source='basic_tour.difficulty_level')
    comfort_level = serializers.IntegerField(source='basic_tour.comfort_level')
    babies_alowed = serializers.BooleanField(source='basic_tour.babies_alowed')
    animals_not_exploited = serializers.BooleanField(source='basic_tour.animals_not_exploited')
    difficulty_description = serializers.CharField(source='basic_tour.difficulty_description')
    property_types = serializers.StringRelatedField(many=True, source='basic_tour.tour_property_types')
    property_images = PropertyImageSerializer(many=True, source='basic_tour.tour_property_images')
    languages = serializers.StringRelatedField(many=True,)
    
    class Meta:
        model = TourAdvanced
        fields = ('rating', 'name', 'wallpaper', 'basic_type', 'additional_types', 'start_region', 'finish_region', 'start_country', 'finish_country', 'start_city', 'finish_city', 'description', 'plan', 'cancellation_terms', 'difficulty_level', 'property_types', 'difficulty_description', 'comfort_level', 'babies_alowed', 'animals_not_exploited', 'property_images', 'start_date', 'finish_date', 'start_time', 'finish_time', 'direct_link', 'instant_booking', 'members_number', 'prepayment', 'postpayment', 'team_member', 'currency', 'cost', 'languages', 'is_guaranteed', 'flight_included', 'scouting',)


class TourBasicListSerializer(serializers.ModelSerializer):
    expert_first_name = serializers.CharField(source='expert.first_name')
    expert_last_name = serializers.CharField(source='expert.last_name')
    expert_rating = serializers.DecimalField(max_digits=2, decimal_places=1, source='expert.rating')
    start_country = serializers.CharField(source='start_country.name')

    class Meta:
        model = TourBasic
        fields = ['name', 'start_country', 'expert_first_name', 'expert_last_name', 'expert_rating']
