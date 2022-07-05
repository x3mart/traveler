from datetime import date
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from geoplaces.serializers import CityFullNameSerializer, CitySerializer, CountrySerializer, RegionSerializer, CountryRegionSerializer
from utils.mixins import TourSerializerMixin
from .models import Important, Tour, TourAccomodation, TourPropertyType, TourType
from currencies.serializers import CurrencySerializer
from accounts.serializers import ExpertListSerializer, TeamMemberSerializer
from languages.serializers import LanguageSerializer
from utils.images import get_image_uri, get_tmb_image_uri


class ImageSerializer(serializers.Serializer):
    tmb_image = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(max_length=255, required=False)
    id = serializers.IntegerField(required=False)
    
    def get_tmb_image(self, obj): 
        return get_tmb_image_uri(self, obj)


class WallpaperSerializer(serializers.Serializer):
    tmb_wallpaper = serializers.SerializerMethodField(read_only=True)
    wallpaper = serializers.ImageField(max_length=255, required=False)
    
    def get_tmb_wallpaper(self, obj): 
        return get_tmb_image_uri(self, obj)


class TourPropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPropertyType
        fields = '__all__'


class TourPropertyTypeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPropertyType
        fields = ['id', 'name']


class TourAccomodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourAccomodation
        fields = '__all__'


class TourAccomodationShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourAccomodation
        fields = ['id', 'name']


class TourTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourType
        fields = '__all__'

class TourTypeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourType
        fields = ('id', 'name')


class ImportantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Important
        fields = '__all__'


TOUR_FIELDS = ('id', 'rating', 'reviews_count', 'name', 'wallpaper', 'tmb_wallpaper', 'basic_type', 'additional_types', 'start_region', 'finish_region', 'start_country', 'finish_country', 'start_russian_region', 'finish_russian_region', 'start_city', 'finish_city', 'description', 'plan', 'cancellation_terms', 'difficulty_level', 'difficulty_description', 'tour_property_types', 'accomodation', 'tour_property_images', 'comfort_level', 'babies_alowed', 'animals_not_exploited', 'start_date', 'finish_date', 'start_time', 'finish_time', 'direct_link', 'instant_booking', 'members_number', 'team_member', 'guest_guide', 'price_comment', 'prepay_amount', 'prepay_in_prc', 'prepay_currency', 'postpay_on_start_day', 'postpay_days_before_start', 'currency', 'price', 'cost', 'discount_starts', 'discount_finish', 'discount_in_prc', 'discount', 'languages', 'is_guaranteed', 'flight_included', 'scouting', 'tour_images', 'tour_days', 'main_impressions', 'tour_included_services', 'tour_excluded_services', 'tour_addetional_services','hotel_name', 'age_starts', 'age_ends', 'media_link', 'week_recurrent', 'month_recurrent', 'vacants_number', 'on_moderation', 'is_active', 'is_draft', 'air_tickets', 'duration', 'sold', 'watched', 'guest_requirements', 'take_with', 'key_features', 'new_to_see', 'map', 'slug') 


class TourPreviewSerializer(serializers.ModelSerializer, TourSerializerMixin):
    basic_type = serializers.StringRelatedField(many=False, read_only=True)
    additional_types = serializers.StringRelatedField(many=True, read_only=True)
    start_region = serializers.StringRelatedField(many=False, read_only=True)
    finish_region = serializers.StringRelatedField(many=False, read_only=True)
    start_country = serializers.StringRelatedField(many=False, read_only=True)
    finish_country = serializers.StringRelatedField(many=False, read_only=True)
    start_russian_region = serializers.StringRelatedField(many=False, read_only=True)
    finish_russian_region = serializers.StringRelatedField(many=False, read_only=True)
    start_city = serializers.StringRelatedField(many=False, read_only=True)
    finish_city = serializers.StringRelatedField(many=False, read_only=True)
    tour_property_types = serializers.StringRelatedField(many=True, read_only=True)
    accomodation = serializers.StringRelatedField(many=True, read_only=True)
    tour_property_images = ImageSerializer(many=True, read_only=True)
    tour_images = ImageSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    currency = CurrencySerializer(many=False, read_only=True)
    expert = ExpertListSerializer(many=False, read_only=True, source='tour_basic.expert')
    team_member = TeamMemberSerializer(many=False, read_only=True)
    tmb_wallpaper = serializers.SerializerMethodField(read_only=True)
    wallpaper = serializers.SerializerMethodField(read_only=True)
    rating = serializers.DecimalField(max_digits=2,decimal_places=1, source='tour_basic.rating',read_only=True)
    reviews_count = serializers.IntegerField(source='tour_basic.reviews_count',read_only=True)
    start_time = serializers.SerializerMethodField(read_only=True)
    finish_time = serializers.SerializerMethodField(read_only=True)
    discounted_price = serializers.SerializerMethodField(read_only=True)
    book_price = serializers.SerializerMethodField(read_only=True)
    daily_price = serializers.SerializerMethodField(read_only=True)
    decline_reasons = serializers.SerializerMethodField(read_only=True)
    postpay_final_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tour
        fields = TOUR_FIELDS + ('expert', 'cost', 'discounted_price', 'book_price', 'daily_price', 'decline_reasons', 'postpay_final_date', 'slug')

    def get_tmb_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_tmb_image_uri(self, obj.wallpaper)
        return None
      
    def get_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_image_uri(self, obj.wallpaper)
        return None
    
    def get_decline_reasons(self, obj):
        if not obj.is_active and obj.decline_reasons.all().exists():
            return obj.decline_reasons.last().reason
        return None
            

class TourSerializer(serializers.ModelSerializer, TourSerializerMixin):
    basic_type = TourTypeSerializer(many=False, read_only=True)
    team_member = TeamMemberSerializer(many=False, read_only=True)
    additional_types = TourTypeSerializer(many=True, read_only=True)
    tour_property_types = TourPropertyTypeSerializer(many=True, read_only=True)
    accomodation = TourAccomodationSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    currency = CurrencySerializer(many=False, read_only=True)
    tour_property_images = ImageSerializer(many=True, read_only=True)
    tour_images = ImageSerializer(many=True, read_only=True)
    main_impressions = serializers.SerializerMethodField(read_only=True)
    tour_included_services = serializers.SerializerMethodField(read_only=True)
    tour_excluded_services = serializers.SerializerMethodField(read_only=True)
    tmb_wallpaper = serializers.SerializerMethodField(read_only=True)
    wallpaper = serializers.SerializerMethodField(read_only=True)
    postpay_on_start_day = serializers.BooleanField(required=False)
    rating = serializers.DecimalField(max_digits=2,decimal_places=1, source='tour_basic.rating',read_only=True)
    reviews_count = serializers.IntegerField(source='tour_basic.reviews_count',read_only=True)
    start_region = RegionSerializer(many=False, read_only=True)
    finish_region = RegionSerializer(many=False, read_only=True)
    start_country = CountrySerializer(many=False, read_only=True)
    finish_country = CountrySerializer(many=False, read_only=True)
    start_russian_region = CountryRegionSerializer(many=False, read_only=True)
    finish_russian_region = CountryRegionSerializer(many=False, read_only=True)
    start_city = CityFullNameSerializer(many=False, read_only=True)
    finish_city = CityFullNameSerializer(many=False, read_only=True)
    postpay_days_before_start = serializers.SerializerMethodField(read_only=True)
    required_fields = serializers.SerializerMethodField(read_only=True)
    decline_reasons = serializers.SerializerMethodField(read_only=True)
    

    class Meta:
        model = Tour
        fields = TOUR_FIELDS + ('completed_sections', 'required_fields', 'decline_reasons')
        extra_kwargs = {
            'animals_not_exploited': {'required': False,},
            'instant_booking': {'required': False,}, 
            'is_draft': {'required': False,},
            'flight_included': {'required': False,},
            'duration': {'required': False, 'read_only':True},
            'slug': {'required': False, 'read_only':True},
        }

    def get_tmb_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_tmb_image_uri(self, obj.wallpaper)
        return None
    
    def get_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_image_uri(self, obj.wallpaper)
        return None
    
    def get_decline_reasons(self, obj):
        if not obj.is_active and obj.decline_reasons.all().exists():
            return obj.decline_reasons.last().reason
        return None
    


class TourListSerializer(serializers.ModelSerializer, TourSerializerMixin):
    tmb_wallpaper = serializers.SerializerMethodField(read_only=True)
    currency = CurrencySerializer(many=False)
    start_country = serializers.StringRelatedField(many=False,)
    start_city = serializers.StringRelatedField(many=False,)
    expert = ExpertListSerializer(many=False, source='tour_basic.expert')
    vacants_number = serializers.SerializerMethodField(read_only=True)
    is_favourite = serializers.SerializerMethodField(read_only=True)
    is_new = serializers.SerializerMethodField(read_only=True)
    is_recomended = serializers.SerializerMethodField(read_only=True)
    discount = serializers.SerializerMethodField(read_only=True)
    discounted_price = serializers.IntegerField(read_only=True)
    api_url = serializers.SerializerMethodField(read_only=True)
    public_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tour
        fields = ['id', 'name', 'start_date', 'start_country', 'start_city', 'price', 'discount', 'duration', 'currency', 'tmb_wallpaper', 'expert', 'vacants_number', 'is_favourite', 'is_new', 'is_recomended', 'discounted_price', 'slug', 'api_url', 'public_url']
    
    def get_tmb_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_tmb_image_uri(self, obj.wallpaper)
        return None
    
    def get_public_url(self, obj):
        print(obj)
        print(obj.slug)
        if obj.start_region.slug == 'rossiia':
            return f'{obj.start_region.slug}/{obj.start_russian_region.slug}/?date_id={obj.id}'
        return f'{obj.start_region.slug}/{obj.start_country.slug}/?date_id={obj.id}'

    def get_api_url(self, obj):
        request = self.context.get('request')
        if obj.start_region.slug == 'rossiia':
            return request.build_absolute_uri(f'{obj.slug}/?date_id={obj.id}')
        return request.build_absolute_uri(f'{obj.slug}/?date_id={obj.id}')


class TourSetSerializer(serializers.ModelSerializer, TourSerializerMixin):
    tmb_wallpaper = serializers.SerializerMethodField(read_only=True)
    currency = CurrencySerializer(many=False)
    start_country = serializers.StringRelatedField(many=False,)
    rating = serializers.DecimalField(max_digits=2,decimal_places=1, source='tour_basic.rating')
    reviews_count = serializers.IntegerField(source='tour_basic.reviews_count')

    class Meta:
        model = Tour
        fields = ['id', 'rating', 'reviews_count', 'name', 'tmb_wallpaper', 'start_date', 'finish_date', 'start_country', 'price', 'cost', 'discount', 'on_moderation', 'is_active', 'is_draft', 'duration', 'sold', 'watched', 'currency', 'slug']
    
    def get_tmb_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_tmb_image_uri(self, obj.wallpaper)
        return None



class FilterSerializer(serializers.Serializer):
    tour_types = TourTypeShortSerializer(many=True)
    languages = LanguageSerializer(many=True)
    property_type =TourPropertyTypeShortSerializer(many=True)
    accomodation = TourAccomodationShortSerializer(many=True)