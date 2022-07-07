from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CityViewSet, DestinationViewSet, RegionViewSet

router = DefaultRouter()

urlpatterns = [
    
]

router.register(r'regions', RegionViewSet, basename='region')
router.register(r'destinations', DestinationViewSet, basename='destination')
router.register(r'cities', CityViewSet, basename='city')

urlpatterns += router.urls