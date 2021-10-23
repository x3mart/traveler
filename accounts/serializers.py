from .models import Expert, User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from utils.translate import get_translatable_fields_source


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
        

class UserSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.fields = get_translatable_fields_source(self) 

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
    
class ExpertSerializer(UserSerializer):

    def __init__(self, *args, **kwargs):
        super(ExpertSerializer, self).__init__(*args, **kwargs)
        self.fields = get_translatable_fields_source(self)
    
    tmb_avatar = serializers.SerializerMethodField(read_only=True)
    tours_count = serializers.IntegerField(read_only=True,)
    tours_avg_rating = serializers.DecimalField(read_only=True, max_digits=2, decimal_places=1)
    class Meta:
        model = Expert
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,},
        }
    
    def get_tmb_avatar(self, obj):
        if obj.tmb_avatar:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.tmb_avatar) 
        return None   
    
    def create(self, validated_data):
        password = check_password(self)
        validated_data['is_expert'] = True
        expert = Expert(**validated_data)
        expert.set_password(password)
        expert.save()
        return expert
    
    def update(self, instance, validated_data):
        validated_data['is_expert'] = True
        if validated_data.get('password') is not None:
            check_password(self)
            password = validated_data.pop('password')
            instance.set_password(password)
            instance.save()    
        return super().update(instance, validated_data)
