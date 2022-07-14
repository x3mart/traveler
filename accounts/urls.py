from rest_framework.routers import DefaultRouter
from .views import ExpertViewSet, IdentifierViewSet, TeamMemberViewSet, UserViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'accounts', UserViewSet, basename='account')
router.register(r'experts', ExpertViewSet, basename='expert')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'teammembers', TeamMemberViewSet, basename='teammember')
router.register(r'identifiers', IdentifierViewSet, basename='identifier')

urlpatterns = router.urls