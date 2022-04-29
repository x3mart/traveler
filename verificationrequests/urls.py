from django.urls import path
from .views import DocumentScanView
urlpatterns = [
    path('scans/', DocumentScanView.as_view(), name='scan'),
    ]
    