from rest_framework import serializers

from geoplaces.models import City, Country, Destination, Region, CountryRegion


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


class DestinationSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    public_url = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Destination
        fields = '__all__'
    
    def get_name(self, obj):
        return obj.country.name if obj.country else obj.country_region.name
    
    def get_public_url(self, obj):
        return f'{obj.country.region.slug}/{obj.country.slug}' if obj.country else f'{obj.country_region.country.region.slug}/{obj.country_region.slug}'
    
    def get_image(self, obj):
        request = self.context['request']
        if obj.country and obj.country.image:
            return request.build_absolute_uri(obj.country.image.url)
        elif obj.country_region and obj.country_region.image:
            return request.build_absolute_uri(obj.country_region.image.url)
        return None
    
