from rest_framework import serializers

from bankdetails.models import BankTransaction, DebetCard

class DebetCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebetCard
        fields = '__all__'


class BankTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransaction
        fields = '__all__'