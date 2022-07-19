from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ActiveDestination, ActiveRegion, ActiveType, MainMenu, StartPage, TourAccomodationTypeViewSet, TourPropertyTypeViewSet, TourTypeViewSet, TourViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'tourtypes', TourTypeViewSet, basename='tourtype')
router.register(r'tourpropertytypes', TourPropertyTypeViewSet, basename='tourpropertytype')
router.register(r'touraccomodations', TourAccomodationTypeViewSet, basename='touraccomodation')

urlpatterns = [
    # path('filter_set/', FilterView.as_view()),
    path('active_regions/', ActiveRegion.as_view()),
    path('active_destinations/', ActiveDestination.as_view()),
    path('active_types/', ActiveType.as_view()),
    path('start_page/', StartPage.as_view()),
    path('main_menu/', MainMenu.as_view())
]

urlpatterns += router.urls