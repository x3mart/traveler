from rest_framework import serializers

from geoplaces.models import City, Destination, Destination, Region, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


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
    rank = serializers.FloatField(read_only=True)
    class Meta:
        model = City
        fields = ['id', 'full_name', 'rank']

    def get_full_name(self, obj):
        destination = f' ({obj.destination.name})' if obj.destination else ''
        region = f' ({obj.destination.region.name})' if obj.destination and obj.destination.region else ''
        return obj.name + region + destination



class DestinationSerializer(serializers.ModelSerializer):
    public_url = serializers.SerializerMethodField(read_only=True)
    tours_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Destination
        fields = '__all__'
    
    def get_public_url(self, obj):
        return f'{obj.region.slug}/{obj.slug}'


class DestinationShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    public_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'slug', 'image', 'alt', 'public_url', 'map_icon']

    def get_public_url(self, obj):
        return f'tours/{obj.slug}'

class RegionShortSerializer(serializers.ModelSerializer):
    destinations = DestinationShortSerializer(many=True)
    class Meta:
        model = Region
        fields = ('id', 'name', 'destinations',)


