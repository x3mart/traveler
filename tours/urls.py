from rest_framework.routers import DefaultRouter
from .views import TourAccomodationTypeViewSet, TourPlanViewSet, TourViewSet, TourTypeViewSet, TourDayViewSet, TourDayImageViewSet, TourPropertyImageViewSet, TourImageViewSet, TourPropertyTypeViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
# router.register(r'basictours', TourBasicViewSet, basename='basictour')
router.register(r'tourtypes', TourTypeViewSet, basename='tourtype')
router.register(r'tourdays', TourDayViewSet, basename='tourday')
router.register(r'tourdayimages', TourDayImageViewSet, basename='tourdayimage')
router.register(r'tourpropertytypes', TourPropertyTypeViewSet, basename='tourpropertytype')
router.register(r'tourpropertyimages', TourPropertyImageViewSet, basename='tourpropertyimage')
router.register(r'tourimages', TourImageViewSet, basename='tourimage')
router.register(r'tourplans', TourPlanViewSet, basename='tourplan')
router.register(r'touraccomodations', TourAccomodationTypeViewSet, basename='touraccomodation')

urlpatterns = router.urls