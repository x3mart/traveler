from datetime import date
from bankdetails.serializers import BankTransactionSerializer, DebetCardSerializer
from dadata import Dadata
from currencies.serializers import CurrencySerializer
from referals.models import Referral
# from tours.models import Tour
from traveler.settings import DADATA_API, DADATA_SECRET
from django.utils import timezone
from languages.serializers import LanguageSerializer
from utils.mixins import TourSerializerMixin
from verificationrequests.serializers import VerificationRequestlSerializer
from .models import Customer, Expert, Identifier, TeamMember, User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from utils.images import get_tmb_image_uri
from djoser.serializers import UidAndTokenSerializer
from djoser import utils


class TourListExpertSerializer(serializers.ModelSerializer, TourSerializerMixin):
    tmb_wallpaper = serializers.SerializerMethodField(read_only=True)
    currency = CurrencySerializer(many=False)
    start_destination = serializers.StringRelatedField(many=False,)
    start_city = serializers.StringRelatedField(many=False,)
    vacants_number = serializers.SerializerMethodField(read_only=True)
    is_new = serializers.SerializerMethodField(read_only=True)
    is_recomended = serializers.SerializerMethodField(read_only=True)
    discount = serializers.SerializerMethodField(read_only=True)
    discounted_price = serializers.IntegerField(read_only=True)
    api_url = serializers.SerializerMethodField(read_only=True)
    public_url = serializers.SerializerMethodField(read_only=True)
    rating = serializers.DecimalField(max_digits=2,decimal_places=1, source='tour_basic.rating',read_only=True)
    is_favorite = serializers.BooleanField(read_only=True)

    class Meta:
        model = Tour
        fields = ['id', 'name', 'start_date', 'start_destination', 'start_city', 'price', 'discount', 'duration', 'currency', 'tmb_wallpaper', 'expert', 'vacants_number', 'is_favorite', 'is_new', 'is_recomended', 'discounted_price', 'slug', 'api_url', 'public_url', 'rating']
    
    def get_tmb_wallpaper(self, obj):
        if obj.wallpaper: 
            return get_tmb_image_uri(self, obj.wallpaper)
        return None
    
    def get_public_url(self, obj):
        return f'tours/{obj.start_region.slug}/{obj.start_destination.slug}/{obj.slug}/?date_id={obj.id}'

    def get_api_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/tours/{obj.slug}/preview/?date_id={obj.id}')



def check_password(self):
    request = self.context['request']
    re_password = request.data.get('re_password')
    password = request.data.get('password')
    if not password:
        raise serializers.ValidationError({'password':[_('Укажите пароль')]})
    if password != re_password:
        raise serializers.ValidationError({'password':[_('Пароли должны совпадать')]})
    try:
        validators.validate_password(password)
    except exceptions.ValidationError as exc:
        raise serializers.ValidationError({'password':exc.messages})
    return password

class EmailActivationSerializer(UidAndTokenSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs


class TeamMemberSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    class Meta:
        model = TeamMember
        fields = '__all__'


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        exclude = ['email', ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'password', 'is_staff', 'avatar', 'phone')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,},
            'email': {'required': False,},
        }
        
    
    def create(self, validated_data):
        password = check_password(self)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        if validated_data.get('password') is not None:
            check_password(self)
            password = validated_data.pop('password')
            instance.set_password(password)
            instance.save()  
        user = super().update(instance, validated_data)
        return user


class ExpertListSerializer(serializers.ModelSerializer):
    tmb_avatar = serializers.SerializerMethodField(read_only=True)
    active_tours = serializers.IntegerField(read_only=True)
    class Meta:
        model = Expert
        fields = ('id', 'first_name', 'last_name', 'tmb_avatar', 'rating', 'active_tours', 'tours_count', 'tours_rating', 'reviews_count', 'tour_reviews_count', 'about')
            
    def get_tmb_avatar(self, obj): 
        return get_tmb_image_uri(self, obj) 


class ExpertSerializer(serializers.ModelSerializer):
    tmb_avatar = serializers.SerializerMethodField(read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    team_members = serializers.SerializerMethodField(read_only=True)
    expert_tours = TourListExpertSerializer(many=True, read_only=True)
    last_visit = serializers.SerializerMethodField(read_only=True)
    registration_date = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Expert
        fields = ('id', 'email', 'first_name', 'last_name', 'avatar', 'tmb_avatar', 'country', 'city', 'languages', 'visited_countries', 'about', 'email_confirmed', 'phone_confirmed', 'docs_confirmed', 'status_confirmed', 'rating', 'tours_count', 'tours_rating', 'reviews_count', 'tour_reviews_count', 'video', 'team_members', 'expert_tours', 'is_online', 'last_visit', 'registration_date')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,},
            'email': {'write_only': True, 'required': True,},
        }
            
    def get_tmb_avatar(self, obj): 
        return get_tmb_image_uri(self, obj) 
    
    def get_last_visit(self, obj):
        if not obj.last_visit:
            return 'очень давно'
        if (timezone.now() - obj.last_visit).days <= 0:
            return obj.last_visit.strftime("в %H:%M")
        return obj.last_visit.strftime('%d %B %Y в %H:%M')
    
    def get_registration_date(self, obj):
        if not obj.registration_date:
            return 'очень давно'
        return obj.last_visit.strftime('%d %B %Yг.')
    
    def get_team_members(self, obj):
        return TeamMemberSerializer(obj.team_members.exclude(is_expert=True) , many=True, context={'request':self.context['request']}).data
    
    def create(self, validated_data):
        request = self.context['request']
        password = check_password(self)
        validated_data['is_expert'] = True
        dadata = Dadata(DADATA_API, DADATA_SECRET)
        result = dadata.clean("name", request.data['name'])
        if result:
            validated_data['first_name'] = result.get('name')
            validated_data['last_name'] = result.get('surname')
        expert = Expert(**validated_data)
        expert.set_password(password)
        expert.save()
        if request.data.get('referral'):
            try:
                beneficiary = User.objects.get(pk=utils.decode_uid(request.data.get('referral')))
                Referral.objects.create(referral_id=expert.id, beneficiary_id=beneficiary.id)
            except:
                pass
        return expert
    
class ExpertMeSerializer(serializers.ModelSerializer):
    tmb_avatar = serializers.SerializerMethodField(read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    debet_card = DebetCardSerializer(many=False, read_only=True)
    bank_transaction = BankTransactionSerializer(many=False, read_only=True)
    verifications = VerificationRequestlSerializer(many=False, read_only=True)
    referral_link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Expert
        fields = ('id', 'password', 'email', 'first_name', 'last_name', 'avatar', 'phone', 'tmb_avatar', 'country', 'city', 'languages', 'visited_countries', 'about', 'email_confirmed', 'phone_confirmed', 'docs_confirmed', 'status_confirmed', 'rating', 'tours_count', 'tours_rating', 'reviews_count', 'tour_reviews_count', 'video', 'commission', 'verifications', 'debet_card', 'bank_transaction', 'preferred_payment_method', 'referral_link', 'referrals_score')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,},
            'avatar': {'read_only': True, 'required': False,},
            'commission': {'read_only': True, 'required': False,},
            'referrals_score': {'read_only': True, 'required': False,},
        }
            
    def get_tmb_avatar(self, obj): 
        return get_tmb_image_uri(self, obj)   
    
    def update(self, instance, validated_data):
        validated_data['is_expert'] = True
        if validated_data.get('password') is not None:
            check_password(self)
            password = validated_data.pop('password')
            instance.set_password(password)
            instance.save()    
        return super().update(instance, validated_data)
        
    def get_tmb_avatar(self, obj): 
        return get_tmb_image_uri(self, obj)
    
    def get_referral_link(self, obj):
        return  utils.encode_uid(obj.id)

class AvatarSerializer(serializers.Serializer):
    tmb_avatar = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.ImageField(max_length=255, required=True)
    
    def get_tmb_avatar(self, obj): 
        return get_tmb_image_uri(self, obj)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'avatar', 'phone')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,},
            'avatar': {'read_only': True, 'required': False,},
        }
    
    def create(self, validated_data):
        request = self.context['request']
        name = request.data.get('name')
        if not name:
            serializers.ValidationError({'name':[_('Пожалуйста представьтесь')]})
        password = check_password(self)
        validated_data['is_customer'] = True
        if len(name.strip().split(' ')) > 1:
            validated_data['first_name'] = name.strip().split(' ')[0]
            validated_data['last_name'] = name.strip().split(' ')[1]
        else:
            validated_data['first_name'] = name
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()
        if request.data.get('referral'):
            try:
                beneficiary = User.objects.get(pk=utils.decode_uid(request.data.get('referral')))
                Referral.objects.create(referral_id=customer.id, beneficiary_id=beneficiary.id)
                Customer.objects.filter(pk=customer.id).update(referrals_score=2200)
            except:
                pass
        return customer        


class CustomerMeSerializer(serializers.ModelSerializer):
    referral_link = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'avatar', 'phone', 'referral_link', 'referrals_score')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,},
            'avatar': {'read_only': True, 'required': False,},
            'referrals_score': {'read_only': True, 'required': False,},
        }
          
 
    def update(self, instance, validated_data):
        if validated_data.get('password') is not None:            
            check_password(self)
            password = validated_data.pop('password')
            instance.set_password(password)
            instance.save()  
        user = super().update(instance, validated_data)
        return user
    
    def get_referral_link(self, obj):
        return  utils.encode_uid(obj.id)


class IdentifierSerializer(serializers.Serializer):
    ident = serializers.UUIDField(read_only=True)