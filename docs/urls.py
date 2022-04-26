from django.urls import path
from .views import LegalDocView

urlpatterns = [
    path('legals/', LegalDocView.as_view(), name='legal')
]