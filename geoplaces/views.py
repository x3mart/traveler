from rest_framework import viewsets
import requests
import time
from traveler.settings import VK_ACCESS_TOKEN
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from geoplaces.models import City, Country, Region, CountryRegion, VKCity
from .serializers import CitySerializer, CountrySerializer, RegionSerializer, CountryRegionSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        instance, created = Region.objects.get_or_create(**data)
        return Response(RegionSerializer(instance).data, status=201)
        

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['region',]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        instance, created = Country.objects.get_or_create(**data)
        return Response(CountrySerializer(instance).data, status=201)


class CountryRegionViewSet(viewsets.ModelViewSet):
    queryset = CountryRegion.objects.all()
    serializer_class = CountryRegionSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        instance, created = CountryRegion.objects.get_or_create(**data)
        return Response(CountryRegionSerializer(instance).data, status=201)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', 'country_region']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        instance, created = City.objects.get_or_create(**data)
        return Response(CitySerializer(instance).data, status=201)

@api_view(['POST'])
def get_vk_countries(request):
    url = 'https://api.vk.com/method/database.getCountries'
    vk_data = {
        'v':'5.131',
        'count':1,
        'need_all':1,
        'access_token':VK_ACCESS_TOKEN,
        'lang':'ru'
    }
    vk_response = requests.post(url, data=vk_data)
    error = vk_response.json().get('error', None)
    if error:
        return Response(error, status=403)
    vk_data['count'] = vk_response.json().get('response')['count']
    # print(vk_data['count'])
    vk_response = requests.post(url, data=vk_data)
    for item in vk_response.json().get('response')['items']:
        country = {}
        country['name'] = item['title']
        country['foreign_id'] = item['id']
        Country.objects.get_or_create(**country)
    # print(vk_response.json())
    return Response({'count':Country.objects.count()}, status=200)

@api_view(['POST'])
def get_vk_country_regions(request):
    url = 'https://api.vk.com/method/database.getRegions'
    vk_data = {
        'v':'5.131',
        'count':1000,
        'access_token':VK_ACCESS_TOKEN,
        'lang':'ru'
    }
    country = Country.objects.get(foreign_id=1)
    vk_data['country_id'] = 1
    vk_response = requests.post(url, data=vk_data)
    error = vk_response.json().get('error', None)
    if error:
        return Response(error, status=403)
    # vk_data['count'] = vk_response.json().get('response')['count']
    for item in vk_response.json().get('response')['items']:
        region = {}
        region['name'] = item['title']
        region['foreign_id'] = item['id']
        region['country'] = country
        CountryRegion.objects.get_or_create(**region)
        # print(country.name)
        # print(vk_data['count'])
    # vk_response = requests.post(url, data=vk_data)
    # 
    # print(vk_response.json())
    return Response({'count':CountryRegion.objects.count()}, status=200)


@api_view(['POST'])
def get_vk_country_cities(request):
    url = 'https://api.vk.com/method/database.getCities'
    vk_data = {
        'v':'5.131',
        'count':1,
        'need_all':1,
        'access_token':VK_ACCESS_TOKEN,
        'lang':'ru'
    }
    country = Country.objects.get(foreign_id=1)
    for region in country.country_regions.all():
        vk_data['country_id'] = 1
        vk_data['region_id'] = region.foreign_id
        vk_response = requests.post(url, data=vk_data)
        error = vk_response.json().get('error', None)
        if error:
            return Response(error, status=403)
        count = vk_response.json().get('response')['count']
        # print(vk_response.json())
        # print(count)
        # print(region.foreign_id)
        x = 0
        while x < count/1000 + 1:
            vk_data['count'] = 1000
            vk_data['offset'] = 1000 * x
            vk_response = requests.post(url, data=vk_data)
            x += 1
            cities = []
            for item in vk_response.json().get('response')['items']:
                city = {}
                city['name'] = item['title']
                city['foreign_id'] = item['id']
                city['country'] = country
                city['country_region'] = region
                cities.append(VKCity(**city))
            VKCity.objects.bulk_create(cities)
            time.sleep(1)
        # print(country.name)
        # print(VKCity.objects.filter(country=country).count())
    # vk_response = requests.post(url, data=vk_data)
    # 
    # print(vk_response.json())
    return Response({'count':VKCity.objects.count()}, status=200)
