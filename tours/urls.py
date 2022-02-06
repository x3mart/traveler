from rest_framework.routers import DefaultRouter
from .views import TourViewSet, TourBasicViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'basictours', TourBasicViewSet, basename='basictour')

urlpatterns = router.urls