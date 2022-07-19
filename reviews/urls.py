from rest_framework.routers import DefaultRouter

from .views import TourReviewViewSet

router = DefaultRouter()
router.register(r'reviews', TourReviewViewSet, basename='review')
urlpatterns = router.urls
