from rest_framework import serializers

from geoplaces.models import City, Country, Region, CountryRegion


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CityShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CityFullNameSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    # distance = serializers.FloatField(read_only=True)
    # similarity = serializers.FloatField(read_only=True)
    rank = serializers.FloatField(read_only=True)
    class Meta:
        model = City
        fields = ['id', 'full_name', 'rank']

    def get_full_name(self, obj):
        country = f' ({obj.country})' if obj.country else ''
        region = f' ({obj.country_region})' if obj.country_region else ''
        return obj.name + region + country

class CountryRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryRegion
        fields = '__all__'


class CountryRegionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryRegion
        fields = ['id', 'name']



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CountryShortSerializer(serializers.ModelSerializer):
    country_regions = CountryRegionShortSerializer(many=True)
    class Meta:
        model = Country
        fields = ['id', 'name', 'country_regions']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class RegionShortSerializer(serializers.ModelSerializer):
    countries = CountryShortSerializer(many=True)
    class Meta:
        model = Region
        fields = ('id', 'name', 'countries')