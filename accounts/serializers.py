from .models import User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from io import BytesIO
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import os


def create_avatar(image, max_width=350, max_height=400):
    size = (max_width, max_height)
    memory_image = BytesIO(image.read())
    pil_image = PilImage.open(memory_image)
    img_format = os.path.splitext(image.name)[1][1:].upper()
    img_format = 'JPEG' if img_format == 'JPG' else img_format

    if pil_image.width > max_width or pil_image.height > max_height:
        pil_image.thumbnail(size)

    new_image = BytesIO()
    pil_image.save(new_image, format=img_format)

    new_image = ContentFile(new_image.getvalue())
    return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)

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
        self.fields['name'] = serializers.CharField(required=True, source=f"name_{self.context['language']}")  

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'is_staff', 'avatar')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,},
        }
        
    
    def create(self, validated_data):
        password = check_password(self)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # if user.avatar:
        #     create_avatar(user.avatar)
        return user
    
    def update(self, instance, validated_data):
        if validated_data.get('password') is not None:
            check_password(self)
            password = validated_data.pop('password')
            instance.set_password(password)
            instance.save()
        if validated_data.get('avatar') is not None:
            validated_data['avatar'] = create_avatar(validated_data['avatar'])
        else:
            validated_data.pop('avatar')     
        user = super().update(instance, validated_data)
        return user