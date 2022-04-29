from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import permissions

from verificationrequests.models import Legal, Scan
from verificationrequests.serializers import LegalSerializer, ScanSerializer
from accounts.models import Expert

# Create your views here.
class DocumentScanView(CreateAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        expert = Expert.objects.get(pk=self.request.user.id)
        serializer.save(expert=expert)


class DocumentScanDestroyView(DestroyAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
    permission_classes = [permissions.IsAuthenticated]
