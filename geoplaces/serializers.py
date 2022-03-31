from rest_framework import serializers

from geoplaces.models import City, Country, Region, CountryRegion


class CitySerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField(many=False)
    country_region = serializers.StringRelatedField(many=False)
    full_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = City
        fields = '__all__'

    def get_full_name(self, obj):
        country = f' ({obj.country})' if obj.country else ''
        region = f' ({obj.country_region})' if obj.country_region else ''
        return obj.name + region + country

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
