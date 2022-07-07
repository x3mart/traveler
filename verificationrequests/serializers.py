from rest_framework import serializers

from geoplaces.serializers import DestinationSerializer
from verificationrequests.models import VerificationRequest




class VerificationRequestlSerializer(serializers.ModelSerializer):
    residency = DestinationSerializer(many=False, read_only=True)
    tours_countries = DestinationSerializer(many=True, read_only=True)
    class Meta:
        model = VerificationRequest
        exclude = ('expert', 'aproved')


# class IndividualSerializer(serializers.ModelSerializer):
#     residency = DestinationSerializer(many=False, read_only=True)
#     tours_countries = DestinationSerializer(many=True, read_only=True)
#     class Meta:
#         model = Individual
#         exclude = ('expert', 'aproved')

