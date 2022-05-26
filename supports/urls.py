from rest_framework.routers import DefaultRouter

from .views import TicketViewSet

router = DefaultRouter()
router.register(r'support_tickets', TicketViewSet, basename='support_ticket')
urlpatterns = router.urls
