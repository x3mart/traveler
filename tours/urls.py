from rest_framework.routers import DefaultRouter
from .views import TourViewSet, TourBasicViewSet, TourTypeViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'basictours', TourBasicViewSet, basename='basictour')
router.register(r'tourtypes', TourTypeViewSet, basename='tourtype')

urlpatterns = router.urls