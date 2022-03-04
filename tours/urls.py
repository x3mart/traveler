from rest_framework.routers import DefaultRouter
from .views import TourAccomodationTypeViewSet, TourGuestGuideImageViewSet, TourPlanImageViewSet, TourPropertyTypeViewSet, TourTypeViewSet, TourViewSet, TourDayImageViewSet, TourPropertyImageViewSet, TourImageViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'tourtypes', TourTypeViewSet, basename='tourtype')
router.register(r'tourdayimages', TourDayImageViewSet, basename='tourdayimage')
router.register(r'tourpropertytypes', TourPropertyTypeViewSet, basename='tourpropertytype')
router.register(r'tourpropertyimages', TourPropertyImageViewSet, basename='tourpropertyimage')
router.register(r'tourimages', TourImageViewSet, basename='tourimage')
router.register(r'tourplanimages', TourPlanImageViewSet, basename='tourplanimage')
router.register(r'tourguestguideimages', TourGuestGuideImageViewSet, basename='tourguestguideimage')
router.register(r'touraccomodations', TourAccomodationTypeViewSet, basename='touraccomodation')

urlpatterns = router.urls