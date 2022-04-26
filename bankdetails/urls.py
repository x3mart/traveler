from django.urls import path
from .views import get_recipient, get_bank

urlpatterns = [
    path('get_bank/', get_bank.as_view(), name='getbank'),
    path('get_recipient/', get_recipient.as_view(), name='get_recipient')
]