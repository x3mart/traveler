from django.urls import path
from rest_framework import generics
from .models import LegalDocument
from .serializers import LegalDocSerializer
from rest_framework.permissions import AllowAny


urlpatterns = [
    path('legals/', generics.ListAPIView.as_view(queryset = LegalDocument.objects.all(), serializer_class = LegalDocSerializer, permission_classes = [AllowAny]), name='legal'),
    path('legals/<slug:docs_slug>/', generics.RetrieveAPIView.as_view(queryset = LegalDocument.objects.all(), serializer_class = LegalDocSerializer, permission_classes = [AllowAny], lookup_field='docs_slug'), name='legal')
]