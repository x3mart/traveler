import json
from unicodedata import name
from rest_framework import viewsets
import requests
import time
from django.db.models.query import Prefetch
from django.db.models import Q, Count
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity, TrigramDistance
from tours.models import Tour
from traveler.settings import VK_ACCESS_TOKEN
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from geoplaces.models import City, Country, Destination, Region
from .serializers import CityFullNameSerializer, CitySerializer, CountrySerializer, DestinationListSerializer, RegionSerializer


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
        

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all().order_by('name')
    serializer_class = DestinationListSerializer
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
        instance, created = Destination.objects.get_or_create(**data)
        return Response(DestinationListSerializer(instance).data, status=201)

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CityFullNameSerializer
    permission_classes = [AllowAny]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['destination']
    # search_fields = ['@name', '^name']
    # ordering_fields = ['name',]
    # ordering = ['name'] 

    def get_queryset(self):
        if self.action == 'list' and not self.request.query_params.get('search'):
            return None
        if self.action == 'list' and self.request.query_params.get('search'):
            search = self.request.query_params.get('search')
            destination = Destination.objects.prefetch_related('region')
            prefetched_destination = Prefetch('destination', destination)
            qs = City.objects.filter(name_ru__trigram_similar=search).annotate(rank=TrigramSimilarity('name_ru', search)).filter(rank__gte=0.3).order_by('-rank').prefetch_related(prefetched_destination)
            return qs
        return super().get_queryset()
    
    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)[:200]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
