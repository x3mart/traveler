from django.urls import path
from .views import get_recipient, get_bank

urlpatterns = [
    path('get_bank/', get_bank, name='getbank'),
    path('get_recipient/', get_recipient, name='get_recipient')
]