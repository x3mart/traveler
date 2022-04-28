from rest_framework import serializers

from bankdetails.models import BankTransaction, DebetCard
from geoplaces.serializers import CountrySerializer

class DebetCardSerializer(serializers.ModelSerializer):
    billing_country = CountrySerializer(many=False, read_only=True)
    class Meta:
        model = DebetCard
        exclude = 'expert'


class BankTransactionSerializer(serializers.ModelSerializer):
    billing_country = CountrySerializer(many=False, read_only=True)
    class Meta:
        model = BankTransaction
        exclude = 'expert'