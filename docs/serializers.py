from rest_framework import serializers
from .models import LegalDocument

class LegalDocSerializer(serializers.ModelSerializer):

    class Meta:
        model = LegalDocument
        fields = '__all__'