from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from geoplaces.models import City, Country, Region, RussianRegion
from .serializers import CitySerializer, CountrySerializer, RegionSerializer, RussianRegionSerializer


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


class RussianRegionViewSet(viewsets.ModelViewSet):
    queryset = RussianRegion.objects.all()
    serializer_class = RussianRegionSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        instance, created = RussianRegion.objects.get_or_create(**data)
        return Response(RussianRegionSerializer(instance).data, status=201)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', 'russian_region']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        instance, created = City.objects.get_or_create(**data)
        return Response(CitySerializer(instance).data, status=201)
