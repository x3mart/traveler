from rest_framework import viewsets

from currencies.serializers import CurrencySerializer
from .models import Currency

class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer