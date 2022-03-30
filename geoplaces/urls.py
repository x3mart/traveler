from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CityViewSet, CountryViewSet, RegionViewSet, CountryRegionViewSet, get_vk_countries, get_vk_country_cities, get_vk_country_regions

router = DefaultRouter()

urlpatterns = [
    path('addcountries/', get_vk_countries, name='addcountry'),
    path('addregions/', get_vk_country_regions, name='addregion'),
    path('addcities/', get_vk_country_cities, name='addcity'),
]

router.register(r'regions', RegionViewSet, basename='region')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'CountryRegions', CountryRegionViewSet, basename='russsianregion')
router.register(r'cities', CityViewSet, basename='city')

urlpatterns += router.urls