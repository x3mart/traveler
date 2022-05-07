from datetime import date
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from geoplaces.serializers import CityFullNameSerializer, CitySerializer, CountrySerializer, RegionSerializer, CountryRegionSerializer
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


class TourAccomodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourAccomodation
        fields = '__all__'


class TourTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourType
        fields = '__all__'


class ImportantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Important
        fields = '__all__'


TOUR_FIELDS = ('id', 'rating', 'reviews_count', 'name', 'wallpaper', 'tmb_wallpaper', 'basic_type', 'additional_types', 'start_region', 'finish_region', 'start_country', 'finish_country', 'start_russian_region', 'finish_russian_region', 'start_city', 'finish_city', 'description', 'plan', 'cancellation_terms', 'difficulty_level', 'difficulty_description', 'tour_property_types', 'accomodation', 'tour_property_images', 'comfort_level', 'babies_alowed', 'animals_not_exploited', 'start_date', 'finish_date', 'start_time', 'finish_time', 'direct_link', 'instant_booking', 'members_number', 'team_member', 'guest_guide', 'price_comment', 'prepay_amount', 'prepay_in_prc', 'prepay_currency', 'postpay_on_start_day', 'postpay_days_before_start', 'currency', 'price', 'cost', 'discount_starts', 'discount_finish', 'discount_in_prc', 'discount', 'languages', 'is_guaranteed', 'flight_included', 'scouting', 'tour_images', 'tour_days', 'main_impressions', 'tour_included_services', 'tour_excluded_services', 'tour_addetional_services','hotel_name', 'age_starts', 'age_ends', 'media_link', 'week_recurrent', 'month_recurrent', 'vacants_number', 'on_moderation', 'is_active', 'is_draft', 'air_tickets', 'duration', 'sold', 'watched', 'guest_requirements', 'take_with', 'key_features', 'new_to_see', 'map') 


TOUR_REQUIRED_FIELDS = {
    'main': ['name', 'wallpaper', 'members_number', 'vacants_number', 'basic_type', 'team_member'],
    'review': ['description',],
    'prices': ['currency', 'price', 'prepay_amount', 'tour_included_services', 'tour_excluded_services', 'air_tickets', 'cancellation_terms'],
    'gallery': ['tour_images'],
    'route': ['start_date', 'finish_date', 'start_city', 'finish_city',],
    'accommodation': ['tour_property_types', 'accomodation', 'tour_property_images'],
    'details': ['languages', 'difficulty_level', 'comfort_level', 'age_starts', 'age_ends'],
    'important': ['take_with']
}


class TourPreviewSerializer(serializers.ModelSerializer):
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
    # important_to_know = ImportantSerializer(read_only=True, many=True)

    class Meta:
        model = Tour
        fields = TOUR_FIELDS + ('expert', 'cost', 'discounted_price', 'book_price', 'daily_price')

    def get_tmb_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_tmb_image_uri(self, obj.wallpaper)
        return None
      
    def get_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_image_uri(self, obj.wallpaper)
        return None

    def get_start_time(self, obj):
        if obj.start_time:
            return obj.start_time.strftime('%H:%M')
        else:
            return None

    def get_finish_time(self, obj):
        if obj.finish_time:
            return obj.finish_time.strftime('%H:%M')
        else:
            return None
    
    def get_discounted_price(self, obj):
        if obj.price and obj.discount and obj.discount_starts and  obj.discount_finish and obj.discount_starts < date.today() and  obj.discount_finish > date.today():
            return round(obj.price - obj.price*(obj.discount/100)) if obj.prepay_in_prc else obj.price - obj.discount
        else:
            return None

    def get_book_price(self, obj): 
        if obj.price:
            return round(obj.price*obj.prepay_amount/100) + 1 if obj.prepay_in_prc else obj.prepay_amount
        return None
    
    def get_daily_price(self, obj):
        discounted_price = self.get_discounted_price(obj)
        if discounted_price:
            return round(discounted_price/obj.duration)
        if obj.price and obj.duration: 
            return round(obj.price/obj.duration)
        return None


class TourSerializer(serializers.ModelSerializer):
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
    

    class Meta:
        model = Tour
        fields = TOUR_FIELDS + ('completed_sections', 'required_fields')
        extra_kwargs = {
            'animals_not_exploited': {'required': False,},
            'instant_booking': {'required': False,}, 
            'is_draft': {'required': False,},
            'flight_included': {'required': False,},
            'duration': {'required': False, 'read_only':True},
        }

    def get_tmb_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_tmb_image_uri(self, obj.wallpaper)
        return None
    
    def get_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_image_uri(self, obj.wallpaper)
        return None
    
    def get_main_impressions(self, obj):
        if obj.main_impressions:
            return '; '.join(obj.main_impressions)
        else:
            return ""
    def get_tour_included_services(self, obj): 
        if obj.tour_included_services:
            return '; '.join(obj.tour_included_services)
        else:
            return ""
    
    def get_tour_excluded_services(self, obj):
        if obj.tour_excluded_services is not None:
            return '; '.join(obj.tour_excluded_services)
        else:
            return "" 
    
    def get_required_fields(self, obj):
        required_fields = []
        for value in TOUR_REQUIRED_FIELDS:
            required_fields += TOUR_REQUIRED_FIELDS[value]
        return required_fields
    
    def get_postpay_days_before_start(self, obj):
        return obj.postpay_days_before_start.days


class TourListSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Tour
        fields = ['id', 'name', 'start_date', 'start_country', 'start_city', 'price', 'discount', 'duration', 'currency', 'tmb_wallpaper', 'expert', 'vacants_number', 'is_favourite', 'is_new', 'is_recomended']
    
    def get_tmb_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_tmb_image_uri(self, obj.wallpaper)
        return None
    
    def get_vacants_number(self, obj):
        return obj.vacants_number if obj.vacants_number < 5 else None
    
    def get_is_favourite(self, obj):
        return  None
    
    def get_is_new(self, obj):
        return  None
    
    def get_is_recomended(self, obj):
        return  None
    
    def get_discount(self, obj):
        if obj.price and obj.discount and obj.discount_starts and  obj.discount_finish and obj.discount_starts < date.today() and  obj.discount_finish > date.today():
            return round(obj.price - obj.price*(obj.discount/100)) if obj.prepay_in_prc else obj.price - obj.discount
        else:
            return None


class TourSetSerializer(serializers.ModelSerializer):
    tmb_wallpaper = serializers.SerializerMethodField(read_only=True)
    currency = CurrencySerializer(many=False)
    start_country = serializers.StringRelatedField(many=False,)
    rating = serializers.DecimalField(max_digits=2,decimal_places=1, source='tour_basic.rating')
    reviews_count = serializers.IntegerField(source='tour_basic.reviews_count')

    class Meta:
        model = Tour
        fields = ['id', 'rating', 'reviews_count', 'name', 'tmb_wallpaper', 'start_date', 'finish_date', 'start_country', 'price', 'cost', 'discount', 'on_moderation', 'is_active', 'is_draft', 'duration', 'sold', 'watched', 'currency']
    
    def get_tmb_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_tmb_image_uri(self, obj.wallpaper)
        return None