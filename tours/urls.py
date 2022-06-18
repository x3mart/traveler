from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import FilterView, TourAccomodationTypeViewSet, TourPropertyTypeViewSet, TourTypeViewSet, TourViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'tourtypes', TourTypeViewSet, basename='tourtype')
router.register(r'tourpropertytypes', TourPropertyTypeViewSet, basename='tourpropertytype')
router.register(r'touraccomodations', TourAccomodationTypeViewSet, basename='touraccomodation')

urlpatterns = [
    path('filter_set/', FilterView.as_view()),
]

urlpatterns += router.urls