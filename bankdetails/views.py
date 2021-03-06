from datetime import datetime
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions
from dadata import Dadata
from bankdetails.models import BankTransaction, Scan
from bankdetails.serializers import ScanSerializer
from traveler.settings import DADATA_API

# # Create your views here.
@api_view(['POST'])
def get_bank(request):
    data = {}
    token = DADATA_API
    dadata = Dadata(token)
    result = dadata.find_by_id("bank", request.data.get('bank_bik'))
    payment_type = request.data.get('payment_type')
    print(result)
    if result:
        data = {
            f'{payment_type}_bank_bik':result[0]['data'].get('bic'),
            f'{payment_type}_bank_name':result[0].get('value'),
            f'{payment_type}_bank_account':result[0]['data'].get('correspondent_account'),
            f'{payment_type}_bank_inn':result[0]['data'].get('inn'),
            f'{payment_type}_bank_kpp':result[0]['data'].get('kpp')
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
            'transaction_recipient_name':result[0].get('value'),
            'transaction_recipient_inn':result[0]['data'].get('inn'),
            'transaction_recipient_kpp':result[0]['data'].get('kpp'),
            'transaction_recipient_ogrn':result[0]['data'].get('ogrn'),
            'transaction_recipient_status':result[0]['data'].get('state')['status'],
            'transaction_recipient_legal_address':result[0]['data']['address']['data']['source'],
            'transaction_recipient_registration_date':datetime.fromtimestamp(result[0]['data'].get('state')['registration_date']/1000).date()
        }
    return Response(data, status=200)

class DocumentScanView(CreateAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        bank_transaction = BankTransaction.objects.get(expert=self.request.user.id)
        serializer.save(bank_transaction=bank_transaction)


class DocumentScanDestroyView(DestroyAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
    permission_classes = [permissions.IsAuthenticated]



# class DebetCardView(viewsets.ModelViewSet):
#     queryset = DebetCard.objects.all()
#     serializer_class = DebetCardSerializer
#     permission_classes = [BankDetailPermission]


# class BankTransactionView(viewsets.ModelViewSet):
#     queryset = BankTransaction.objects.all()
#     serializer_class = BankTransactionSerializer
#     permission_classes = [BankDetailPermission]