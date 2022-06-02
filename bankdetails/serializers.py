from rest_framework import serializers

from bankdetails.models import Scan, DebetCard, BankTransaction


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        exclude = ('bank_transaction',)


class DebetCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebetCard
        exclude = ('expert',)


class BankTransactionSerializer(serializers.ModelSerializer):
    scans = ScanSerializer(many=True, read_only=True)
    class Meta:
        model = BankTransaction
        exclude = ('expert',)
