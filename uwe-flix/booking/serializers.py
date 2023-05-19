from rest_framework import serializers

class GuestStripeInformationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    unit_amount = serializers.IntegerField()
    quantity = serializers.IntegerField()