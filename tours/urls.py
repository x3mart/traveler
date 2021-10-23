from rest_framework.routers import DefaultRouter
from .views import TourBasicViewSet

router = DefaultRouter()
router.register(r'tours', TourBasicViewSet, basename='account')

urlpatterns = router.urls