from rest_framework.routers import DefaultRouter
from .views import ExpertViewSet, UserViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'accounts', UserViewSet, basename='account')
router.register(r'experts', ExpertViewSet, basename='expert')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = router.urls