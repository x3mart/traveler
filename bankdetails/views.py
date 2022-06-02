from datetime import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from bankdetails.serializers import BankTransactionSerializer, DebetCardSerializer
from dadata import Dadata
# from bankdetails.models import Scan
from traveler.settings import DADATA_API

# # Create your views here.
@api_view(['POST'])
def get_bank(request):
    data = {}
    token = DADATA_API
    dadata = Dadata(token)
    result = dadata.find_by_id("bank", request.data.get('bank_bik'))
    if result:
        data = {
            'bank_bik':result[0]['data'].get('bic'),
            'bank_name':result[0].get('value'),
            'bank_account':result[0]['data'].get('correspondent_account'),
            'bank_inn':result[0]['data'].get('inn'),
            'bank_kpp':result[0]['data'].get('kpp')
        }
    return Response(data, status=200)

@api_view(['POST'])
def get_recipient(request):
    data = {}
    token = DADATA_API
    dadata = Dadata(token)
    result = dadata.find_by_id("party", request.data.get('recipient_inn'))
    if result:
        data = {
            'recipient_name':result[0].get('value'),
            'recipient_inn':result[0]['data'].get('inn'),
            'recipient_kpp':result[0]['data'].get('kpp'),
            'recipient_ogrn':result[0]['data'].get('ogrn'),
            'recipient_status':result[0]['data'].get('state')['status'],
            'recipient_legal_address':result[0]['data']['address']['data']['source'],
            'recipient_registration_date':datetime.fromtimestamp(result[0]['data'].get('state')['registration_date']/1000).date()
        }
    return Response(data, status=200)

# class DocumentScanView(CreateAPIView):
#     queryset = Scan.objects.all()
#     serializer_class = ScanSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         expert = Expert.objects.get(pk=self.request.user.id)
#         serializer.save(expert=expert)


# class DocumentScanDestroyView(DestroyAPIView):
#     queryset = Scan.objects.all()
#     serializer_class = ScanSerializer
#     permission_classes = [permissions.IsAuthenticated]



# class DebetCardView(viewsets.ModelViewSet):
#     queryset = DebetCard.objects.all()
#     serializer_class = DebetCardSerializer
#     permission_classes = [BankDetailPermission]


# class BankTransactionView(viewsets.ModelViewSet):
#     queryset = BankTransaction.objects.all()
#     serializer_class = BankTransactionSerializer
#     permission_classes = [BankDetailPermission]