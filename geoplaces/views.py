import json
from unicodedata import name
from rest_framework import viewsets
import requests
import time
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity, TrigramDistance
from traveler.settings import VK_ACCESS_TOKEN
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from geoplaces.models import City, Country, Region, CountryRegion, VKCity
from .serializers import CityFullNameSerializer, CitySerializer, CountrySerializer, RegionSerializer, CountryRegionSerializer


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
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['region',]
    search_fields = ['@name', '^name']

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
    serializer_class = CityFullNameSerializer
    permission_classes = [AllowAny]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['country', 'country_region']
    # search_fields = ['@name', '^name']
    # ordering_fields = ['name',]
    # ordering = ['name'] 

    def get_queryset(self):
        if self.action == 'list' and not self.request.query_params.get('search'):
            return None
        if self.action == 'list' and self.request.query_params.get('search'):
            search = self.request.query_params.get('search')
            qs = City.objects.filter(name_ru__trigram_similar=search).annotate(rank=TrigramSimilarity('name_ru', search),).filter(rank__gte=0.3).order_by('-rank').prefetch_related('country', 'country_region')
            return qs
        return super().get_queryset()
    
    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)[:200]


def get_vk_countries():
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
    vk_response = requests.post(url, data=vk_data)
    for item in vk_response.json().get('response')['items']:
        country = {}
        country['name'] = item['title']
        country['foreign_id'] = item['id']
        Country.objects.get_or_create(**country)
    return Country.objects.count()

def get_vk_some(method, region_id=None, lang='en', country=1):
    url = f'https://api.vk.com/method/database.{method}'
    vk_data = {
        'v':'5.131',
        'count':10,
        'need_all':1,
        'access_token':VK_ACCESS_TOKEN,
        'lang':lang,
        'region_id':region_id,
        'country_id':country
    }
    vk_response = requests.post(url, data=vk_data)
    error = vk_response.json().get('error', None)
    if error:
        return print(error)
    print(vk_response.json().get('response'))
    return None

def get_vk_country_regions():
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
    for item in vk_response.json().get('response')['items']:
        region = {}
        region['name'] = item['title']
        region['foreign_id'] = item['id']
        region['country'] = country
        CountryRegion.objects.get_or_create(**region)
    return CountryRegion.objects.count()

def get_vk_country_cities():
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
        print(count)
        print(region.name)
        x = 0
        while x < count/500 + 1:
            vk_data['count'] = 500
            vk_data['offset'] = 500 * x
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
    return VKCity.objects.count()

def set_russian_cities():
    country = Country.objects.get(foreign_id=1)
    for region in country.country_regions.all():
        names = region.vkcities.values("name").distinct()
        print(region.vkcities.count() - names.count())
        print(region.name)
        cities = []
        for item in names:
            city = {}
            city['name'] = item['name']
            city['country'] = country
            city['country_region'] = region
            cities.append(City(**city))
        City.objects.bulk_create(cities)
    return country.cities.count()


def parse_country_json():
    with open('pb_country.json', 'r') as data:
        countries = json.load(data)['countries']
        print(len(countries))
        locations = {country["location"] for country in countries if country["location"] != ''}
        regions = [Region(name=location) for location in locations]
        Region.objects.bulk_create(regions)
        countries_w_region = []
        for region in Region.objects.all():
            countries_w_region += [Country(name=country['name'], name_en=country['english'], counry_code=country['id'], region=region) for country in countries if country["location"] == region.name and country["id"] != 'RU' and country["id"] != 'UA']
        countries_wo_region = [Country(name=country['name'], name_en=country['english'], counry_code=country['id']) for country in countries if country["location"] == '' and country["id"] != 'RU' and country["id"] != 'UA']
        countries = countries_w_region + countries_wo_region
        Country.objects.bulk_create(countries)
        print(Country.objects.count())

def parse_city_json():
    with open('pb_city.json', 'r') as data:
        cities = json.load(data)['cities']
        alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        cities = [city for city in cities if city["country"] != "RU" and city["country"] != "UA" and not alphabet.isdisjoint(city["name"].lower())]
        for country in Country.objects.exclude(counry_code='RU').exclude(counry_code='UA'):
            cities_w_country = list({city['name']:city for city in cities if city["country"] == country.counry_code}.values()) 
            cities_w_country = [City(country=country, name=city['name'], name_en=city['english'], foreign_id=city['id']) for city in cities_w_country]
            City.objects.bulk_create(cities_w_country)
            print(len(cities_w_country))
            print(country.name)

def set_distinct_city():
    for city in City.objects.all():
        cs = City.objects.filter(name=city.name).filter(country=city.country).filter(country_region=city.country_region)
        if cs.count() > 1:
            cs.exclude(pk=city.id).delete()
            print(city.name)
            print(cs.count())



