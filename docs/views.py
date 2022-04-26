from rest_framework import generics
from .models import LegalDocument
from .serializers import LegalDocSerializer
from rest_framework.permissions import AllowAny


# Create your views here.
class LegalDocView(generics.RetrieveAPIView):
    queryset = LegalDocument.objects.all()
    serializer_class = LegalDocSerializer
    permission_classes = [AllowAny]