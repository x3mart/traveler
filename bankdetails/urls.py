from django.urls import path
from .views import DocumentScanDestroyView, DocumentScanView, get_recipient, get_bank

urlpatterns = [
    path('get_bank/', get_bank, name='getbank'),
    path('get_recipient/', get_recipient, name='get_recipient'),
    path('scans/', DocumentScanView.as_view(), name='scan'),
    path('scans/<int:pk>/', DocumentScanDestroyView.as_view(), name='scan'),
]