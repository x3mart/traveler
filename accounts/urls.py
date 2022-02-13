from rest_framework.routers import DefaultRouter
from .views import ExpertViewSet, TeamMemberViewSet, UserViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'accounts', UserViewSet, basename='account')
router.register(r'experts', ExpertViewSet, basename='expert')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'teammembers', TeamMemberViewSet, basename='teammember')

urlpatterns = router.urls