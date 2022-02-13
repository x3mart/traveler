from rest_framework.routers import DefaultRouter
from .views import CityViewSet, CountryViewSet, RegionViewSet, RussianRegionViewSet

router = DefaultRouter()

router.register(r'regions', RegionViewSet, basename='region')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'russianregions', RussianRegionViewSet, basename='russsianregion')
router.register(r'cities', CityViewSet, basename='city')

urlpatterns = router.urls