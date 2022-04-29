from rest_framework import serializers
from .models import Legal, Individual


class LegalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legal
        exclude = ('expert', 'aproved')


class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        exclude = ('expert', 'aproved')