from rest_framework import serializers

from geoplaces.models import City, Country, Region, CountryRegion


class CitySerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField(many=False)
    country_region = serializers.StringRelatedField(many=False)
    class Meta:
        model = City
        fields = '__all__'


class CountryRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryRegion
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
