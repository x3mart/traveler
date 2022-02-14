from dataclasses import fields
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from accounts.models import Expert
from accounts.serializers import ExpertListSerializer, TeamMemberSerializer
from .models import Tour, TourDay, TourDayImage, TourExcludedService, TourImpression, TourIncludedService, TourPropertyImage, TourImage, TourPropertyType, TourType
from geoplaces.serializers import RegionSerializer, CountrySerializer, RussianRegionSerializer, CitySerializer
from languages.serializers import LanguageSerializer
from currencies.serializers import CurrencySerializer



class TourPropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPropertyImage
        fields = '__all__'


class TourPropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPropertyImage
        fields = '__all__'

class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = '__all__'

class TourDayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDayImage
        fields = '__all__'

class TourDaySerializer(serializers.ModelSerializer):
    tour_day_images = TourDayImageSerializer(read_only=True, many=True)
    class Meta:
        model = TourDay
        fields = '__all__'

class TourTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourType
        fields = '__all__'


class TourImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImpression
        fields = '__all__'


class TourIncludedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourIncludedService
        fields = '__all__'


class TourExcludedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourExcludedService
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    basic_type = TourTypeSerializer(many=False, read_only=True)
    additional_types = TourTypeSerializer(many=True, read_only=True)
    start_region = RegionSerializer(many=False, read_only=True)
    finish_region = RegionSerializer(many=False, read_only=True)
    start_country = CountrySerializer(many=False, read_only=True)
    finish_country = CountrySerializer(many=False, read_only=True)
    start_russian_region = RussianRegionSerializer(many=False, read_only=True)
    finish_russian_region = RussianRegionSerializer(many=False, read_only=True)
    start_city = CitySerializer(many=False, read_only=True)
    finish_city = CitySerializer(many=False, read_only=True)
    tour_property_types = TourPropertyTypeSerializer(many=True, read_only=True)
    tour_property_images = TourPropertyImageSerializer(many=True, read_only=True)
    tour_images = TourImageSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    currency = CurrencySerializer(many=False, read_only=True)
    expert = ExpertListSerializer(many=False, read_only=True)
    team_member = TeamMemberSerializer(many=False, read_only=True)
    tour_days = TourDaySerializer(many=True, read_only=True)
    tour_impressions = TourImpressionSerializer(many=True, read_only=True)
    tour_included_services = TourIncludedServiceSerializer(many=True, read_only=True)
    tour_excluded_services = TourExcludedServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = ('id', 'rating', 'reviews_count', 'name', 'wallpaper', 'basic_type', 'additional_types', 'start_region', 'finish_region', 'start_country', 'finish_country', 'start_russian_region', 'finish_russian_region', 'start_city', 'finish_city', 'description', 'plan', 'cancellation_terms', 'difficulty_level', 'difficulty_description', 'tour_property_types', 'tour_property_images', 'comfort_level', 'babies_alowed', 'animals_not_exploited', 'start_date', 'finish_date', 'start_time', 'finish_time', 'direct_link', 'instant_booking', 'members_number', 'prepayment', 'postpayment', 'team_member', 'price_comment', 'prepay_amount', 'prepay_in_prc', 'prepay_currency', 'prepay_starts', 'prepay_finish', 'postpay_on_start_day', 'postpay_days_before_start', 'currency', 'price', 'cost', 'discount', 'languages', 'is_guaranteed', 'flight_included', 'scouting', 'tour_images', 'expert', 'tour_days', 'tour_impressions', 'tour_included_services', 'tour_excluded_services', )


class TourListSerializer(serializers.ModelSerializer):
    expert = ExpertListSerializer(many=False,)
    start_country = serializers.StringRelatedField(many=False,)
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
