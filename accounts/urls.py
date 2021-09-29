from rest_framework.routers import DefaultRouter
from .views import ExpertViewSet, UserViewSet

router = DefaultRouter()
router.register(r'accounts', UserViewSet, basename='account')
router.register(r'experts', ExpertViewSet, basename='expert')

urlpatterns = router.urls