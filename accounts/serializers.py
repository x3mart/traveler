from .models import Customer, Expert, User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import django.contrib.auth.password_validation as validators
from django.core import exceptions


def check_password(self):
    request = self.context['request']
    re_password = request.data.get('re_password')
    password = request.data.get('password')
    if not password:
        raise serializers.ValidationError(_('Укажите пароль'))
    if password != re_password:
        raise serializers.ValidationError(_('Пароли должны совпадать'))
    try:
        validators.validate_password(password)
    except exceptions.ValidationError as exc:
        raise serializers.ValidationError(str(exc))
    return password


def get_tmb_avatar_uri(self, obj):
        if obj.tmb_avatar:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.tmb_avatar) 
        return None         

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'password', 'is_staff', 'avatar', 'phone')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,},
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
    class Meta:
        model = Expert
        fields = ('id', 'first_name', 'last_name', 'tmb_avatar', 'rating', 'tours_count', 'tours_rating', 'reviews_count', 'tour_reviews_count',)
            
    def get_tmb_avatar(self, obj): 
        return get_tmb_avatar_uri(self, obj) 


class ExpertSerializer(serializers.ModelSerializer):
    tmb_avatar = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Expert
        fields = ('id', 'first_name', 'last_name', 'avatar', 'tmb_avatar', 'country', 'city', 'languages', 'visited_countries', 'about', 'email_confirmed', 'phone_confirmed', 'docs_confirmed', 'status_confirmed', 'rating', 'tours_count', 'tours_rating', 'reviews_count', 'tour_reviews_count',)
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,},
        }
            
    def get_tmb_avatar(self, obj): 
        return get_tmb_avatar_uri(self, obj) 
    
    def create(self, validated_data):
        print('create')
        password = check_password(self)
        validated_data['is_expert'] = True
        expert = Expert(**validated_data)
        expert.set_password(password)
        expert.save()
        return expert
    
class ExpertMeSerializer(serializers.ModelSerializer):
    tmb_avatar = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Expert
        fields = ('id','email', 'first_name', 'last_name', 'avatar', 'phone', 'tmb_avatar', 'country', 'city', 'languages', 'visited_countries', 'about', 'email_confirmed', 'phone_confirmed', 'docs_confirmed', 'status_confirmed', 'rating', 'tours_count', 'tours_rating', 'reviews_count', 'tour_reviews_count',)
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,},
        }
            
    def get_tmb_avatar(self, obj): 
        return get_tmb_avatar_uri(self, obj)   
    
    def update(self, instance, validated_data):
        validated_data['is_expert'] = True
        
        if validated_data.get('password') is not None:
            check_password(self)
            password = validated_data.pop('password')
            instance.set_password(password)
            instance.save()    
        return super().update(instance, validated_data)


class CustomerMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'avatar', 'phone')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,},
        }
        
    
    def create(self, validated_data):
        password = check_password(self)
        validated_data['is_customer'] = True
        user = Customer(**validated_data)
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

class CustomerSerializer(serializers.ModelSerializer):
    tmb_avatar = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'avatar', 'tmb_avatar')
    
    def get_tmb_avatar(self, obj): 
        return get_tmb_avatar_uri(self, obj)