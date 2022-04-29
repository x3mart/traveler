from rest_framework import serializers

from geoplaces.serializers import CountrySerializer
from .models import Legal, Individual


class LegalSerializer(serializers.ModelSerializer):
    residency = CountrySerializer(many=False, read_only=True)
    tours_countries = CountrySerializer(many=True, read_only=True)
    class Meta:
        model = Legal
        exclude = ('expert', 'aproved')


class IndividualSerializer(serializers.ModelSerializer):
    residency = CountrySerializer(many=False, read_only=True)
    tours_countries = CountrySerializer(many=True, read_only=True)
    class Meta:
        model = Individual
        exclude = ('expert', 'aproved')