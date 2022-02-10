from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LanguageViewSet, LanguageView

urlpatterns = [
    path('addlangs/', LanguageView.as_view(), name='addlang'),

]
router = DefaultRouter()
router.register(r'languages', LanguageViewSet, basename='language')

urlpatterns += router.urls
