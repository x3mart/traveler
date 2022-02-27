from dataclasses import fields
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from accounts.models import Expert
from accounts.serializers import ExpertListSerializer, TeamMemberSerializer
from .models import Tour, TourDay, TourDayImage, TourExcludedService, TourImpression, TourIncludedService, TourPlan, TourPropertyImage, TourImage, TourPropertyType, TourType
from geoplaces.serializers import RegionSerializer, CountrySerializer, RussianRegionSerializer, CitySerializer
from languages.serializers import LanguageSerializer
from currencies.serializers import CurrencySerializer
from utils.images import get_tmb_image_uri



class TourPropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPropertyType
        exclude = ['tours',]


class TourPropertyImageSerializer(serializers.ModelSerializer):
    tmb_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = TourPropertyImage
        fields = '__all__'
    
    def get_tmb_image(self, obj): 
        return get_tmb_image_uri(self, obj)

class TourImageSerializer(serializers.ModelSerializer):
    tmb_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = TourImage
        fields = '__all__'
    
    def get_tmb_image(self, obj): 
        return get_tmb_image_uri(self, obj)

class TourDayImageSerializer(serializers.ModelSerializer):
    tmb_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = TourDayImage
        fields = '__all__'
    
    def get_tmb_image(self, obj): 
        return get_tmb_image_uri(self, obj)


class TourPlanSerializer(serializers.ModelSerializer):
    tmb_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = TourPlan
        fields = '__all__'
    
    def get_tmb_image(self, obj): 
        return get_tmb_image_uri(self, obj)


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
    # basic_type = TourTypeSerializer(many=False, read_only=True)
    # additional_types = TourTypeSerializer(many=True, read_only=True)
    # start_region = RegionSerializer(many=False, read_only=True)
    # finish_region = RegionSerializer(many=False, read_only=True)
    # start_country = CountrySerializer(many=False, read_only=True)
    # finish_country = CountrySerializer(many=False, read_only=True)
    # start_russian_region = RussianRegionSerializer(many=False, read_only=True)
    # finish_russian_region = RussianRegionSerializer(many=False, read_only=True)
    # start_city = CitySerializer(many=False, read_only=True)
    # finish_city = CitySerializer(many=False, read_only=True)
    # tour_property_types = TourPropertyTypeSerializer(many=True, read_only=True)
    tour_property_images = TourPropertyImageSerializer(many=True, read_only=True)
    tour_images = TourImageSerializer(many=True, read_only=True)
    # languages = LanguageSerializer(many=True, read_only=True)
    # currency = CurrencySerializer(many=False, read_only=True)
    # expert = ExpertListSerializer(many=False, read_only=True, source='tour_basic.expert')
    # team_member = TeamMemberSerializer(many=False, read_only=True)
    tour_days = TourDaySerializer(many=True, read_only=True)
    plan = TourPlanSerializer(many=True, read_only=True)
    main_impressions = serializers.SerializerMethodField(read_only=True)
    tour_included_services = serializers.SerializerMethodField(read_only=True)
    tour_excluded_services = serializers.SerializerMethodField(read_only=True)
    tmb_wallpaper = serializers.SerializerMethodField(read_only=True)
    prepay_in_prc = serializers.SerializerMethodField(read_only=True)
    discount_in_prc = serializers.SerializerMethodField(read_only=True)
    postpay_on_start_day = serializers.BooleanField(required=False)
    rating = serializers.DecimalField(max_digits=2,decimal_places=1, source='tour_basic.rating',read_only=True)
    reviews_count = serializers.IntegerField(source='tour_basic.reviews_count',read_only=True)
    direct_link = serializers.BooleanField(source='tour_basic.direct_link',read_only=True)

    class Meta:
        model = Tour
        fields = ('id', 'rating', 'reviews_count', 'name', 'wallpaper', 'tmb_wallpaper', 'basic_type', 'additional_types', 'start_region', 'finish_region', 'start_country', 'finish_country', 'start_russian_region', 'finish_russian_region', 'start_city', 'finish_city', 'description', 'plan', 'cancellation_terms', 'difficulty_level', 'difficulty_description', 'tour_property_types', 'accomodation', 'tour_property_images', 'comfort_level', 'babies_alowed', 'animals_not_exploited', 'start_date', 'finish_date', 'start_time', 'finish_time', 'direct_link', 'instant_booking', 'members_number', 'team_member', 'price_comment', 'prepay_amount', 'prepay_in_prc', 'prepay_currency', 'postpay_on_start_day', 'postpay_days_before_start', 'currency', 'price', 'cost', 'discount_starts', 'discount_finish', 'discount_in_prc', 'discount', 'languages', 'is_guaranteed', 'flight_included', 'scouting', 'tour_images', 'tour_days', 'main_impressions', 'tour_included_services', 'tour_excluded_services', 'hotel_name', 'age_starts', 'age_ends', 'media_link', 'week_recurrent', 'month_recurrent', 'vacants_number', 'on_moderation', 'is_active', 'is_draft', 'air_tickets', 'duration') 
        extra_kwargs = {
            'tour_property_types': {'required': False, 'read_only':True},
            'additional_types': {'required': False, 'read_only':True},
            'languages': {'required': False, 'read_only':True},
            'animals_not_exploited': {'required': False,},
            'instant_booking': {'required': False,},
            'direct_link': {'required': False,},
            'is_draft': {'required': False,},
            'flight_included': {'required': False,},
        }

    def get_tmb_wallpaper(self, obj): 
        return get_tmb_image_uri(self, obj)
    
    def get_main_impressions(self, obj): 
        main_impressions = obj.main_impressions.all().values_list('name', flat=True)
        return ', '.join(main_impressions)
    
    def get_tour_included_services(self, obj): 
        tour_included_services = obj.tour_included_services.all().values_list('name', flat=True)
        return ', '.join(tour_included_services)
    
    def get_tour_excluded_services(self, obj): 
        tour_excluded_services = obj.tour_excluded_services.all().values_list('name', flat=True)
        return ', '.join(tour_excluded_services)

    def get_prepay_in_prc(self, obj): 
        return 1 if obj.prepay_in_prc else 0
    
    def get_discount_in_prc(self, obj): 
        return 1 if obj.prepay_in_prc else 0


class TourListSerializer(serializers.ModelSerializer):
    expert = ExpertListSerializer(many=False, source='tour_basic.expert')
    start_country = serializers.StringRelatedField(many=False,)
    rating = serializers.DecimalField(max_digits=2,decimal_places=1, source='tour_basic.rating')
    reviews_count = serializers.IntegerField(source='tour_basic.reviews_count')
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
