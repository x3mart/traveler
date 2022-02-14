from rest_framework.routers import DefaultRouter
from .views import TourViewSet, TourTypeViewSet, TourDayViewSet, TourDayImageViewSet, TourPropertyImageViewSet, TourImageViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
# router.register(r'basictours', TourBasicViewSet, basename='basictour')
router.register(r'tourtypes', TourTypeViewSet, basename='tourtype')
router.register(r'tourdays', TourDayViewSet, basename='tourday')
router.register(r'tourdayimages', TourDayImageViewSet, basename='tourdayimage')
router.register(r'tourpropertyimages', TourPropertyImageViewSet, basename='tourpropertyimage')
router.register(r'tourimages', TourImageViewSet, basename='tourimage')

urlpatterns = router.urls