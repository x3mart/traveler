from rest_framework import serializers
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