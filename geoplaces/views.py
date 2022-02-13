from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from geoplaces.models import City, Country, Region, RussianRegion
from .serializers import CitySerializer, CountrySerializer, RegionSerializer, RussianRegionSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]


class RussianRegionViewSet(viewsets.ModelViewSet):
    queryset = RussianRegion.objects.all()
    serializer_class = RussianRegionSerializer
    permission_classes = [AllowAny]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
