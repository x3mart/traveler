from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import permissions

from verificationrequests.models import Legal
from verificationrequests.serializers import LegalSerializer

# Create your views here.
class DocumentScanView(CreateAPIView):
    queryset = Legal.objects.all()
    serializer_class = LegalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        expert = Legal.objects.get(pk=self.request.user.id)
        serializer.save(expert=expert)
