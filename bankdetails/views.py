from datetime import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from bankdetails.serializers import BankTransactionSerializer, DebetCardSerializer
from dadata import Dadata
from traveler.settings import DADATA_API

# # Create your views here.
@api_view(['POST'])
def get_bank(request):
    token = DADATA_API
    dadata = Dadata(token)
    result = dadata.find_by_id("bank", request.data.get('bank_bik'))
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
    token = DADATA_API
    dadata = Dadata(token)
    result = dadata.find_by_id("party", request.data.get('recipient_inn'))
    data = {
        'recipient_name':result[0].get('value'),
        'recipient_inn':result[0]['data'].get('inn'),
        'recipient_kpp':result[0]['data'].get('kpp'),
        'recipient_ogrn':result[0]['data'].get('ogrn'),
        'recipient_status':result[0]['data'].get('state')['status'],
        'recipient_registration_date':datetime.fromtimestamp(result[0]['data'].get('state')['registration_date']/1000).date()
    }
    return Response(data, status=200)



# class DebetCardView(viewsets.ModelViewSet):
#     queryset = DebetCard.objects.all()
#     serializer_class = DebetCardSerializer
#     permission_classes = [BankDetailPermission]


# class BankTransactionView(viewsets.ModelViewSet):
#     queryset = BankTransaction.objects.all()
#     serializer_class = BankTransactionSerializer
#     permission_classes = [BankDetailPermission]