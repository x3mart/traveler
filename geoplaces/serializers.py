from rest_framework import serializers

from geoplaces.models import City, Country, Region, RussianRegion


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RussianRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RussianRegion
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
