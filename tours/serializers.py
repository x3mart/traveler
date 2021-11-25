from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from accounts.models import Expert
from .models import TourAdvanced, TourBasic, TourDay, TourPropertyImage, TourImage


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPropertyImage
        exclude = ('tour',)

class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        exclude = ('tour',)


class TourExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = ('first_name', 'last_name', 'about', 'rating', 'tours_count', 'tours_rating', 'reviews_count', 'tour_reviews_count', 'avatar')


class TourDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDay
        exclude = ('tour',)


class TourSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(decimal_places=1, max_digits=2, source='basic_tour.rating')
    reviews_count = serializers.IntegerField(source='basic_tour.reviews_count')
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
    tour_images = TourImageSerializer(many=True, source='basic_tour.tour_images', partial=True, required=False)
    languages = serializers.StringRelatedField(many=True,)
    currency = serializers.StringRelatedField(many=False, source='currency.short_name')
    expert = TourExpertSerializer(many=False, source='basic_tour.expert')
    tour_days = TourExpertSerializer(many=True, source='basic_tour.tour_days')
    tour_impressions = serializers.StringRelatedField(many=True, source='basic_tour.tour_impressions')
    tour_included_services = serializers.StringRelatedField(many=True, source='basic_tour.tour_included_services')
    tour_excluded_services = serializers.StringRelatedField(many=True, source='basic_tour.tour_excluded_services')

    class Meta:
        model = TourAdvanced
        fields = ('id', 'rating', 'reviews_count', 'name', 'wallpaper', 'basic_type', 'additional_types', 'start_region', 'finish_region', 'start_country', 'finish_country', 'start_city', 'finish_city', 'description', 'plan', 'cancellation_terms', 'difficulty_level', 'property_types', 'difficulty_description', 'comfort_level', 'babies_alowed', 'animals_not_exploited', 'property_images', 'start_date', 'finish_date', 'start_time', 'finish_time', 'direct_link', 'instant_booking', 'members_number', 'prepayment', 'postpayment', 'team_member', 'currency', 'cost', 'languages', 'is_guaranteed', 'flight_included', 'scouting', 'tour_images', 'expert', 'tour_days', 'tour_impressions', 'tour_included_services', 'tour_excluded_services',)


class TourListSerializer(serializers.ModelSerializer):
    expert = TourExpertSerializer(many=False, source='basic_tour.expert')
    rating = serializers.DecimalField(decimal_places=1, max_digits=2, source='basic_tour.rating')
    reviews_count = serializers.IntegerField(source='basic_tour.reviews_count')
    name = serializers.CharField(source='basic_tour.name')
    tmb_wallpaper = serializers.ImageField(source='basic_tour.tmb_wallpaper')
    start_country = serializers.StringRelatedField(many=False, source='basic_tour.start_country')
    class Meta:
        model = TourAdvanced
        fields = ['id', 'rating', 'reviews_count', 'name', 'tmb_wallpaper', 'start_date', 'finish_date', 'start_country',  'expert',]
