from django.urls import path
from .views import DocumentScanView, DocumentScanDestroyView
urlpatterns = [
    path('scans/', DocumentScanView.as_view(), name='scan'),
    path('scans/<int:pk>/', DocumentScanDestroyView.as_view(), name='scan'),
    ]
    