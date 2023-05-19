from rest_framework import serializers

class StripeInformation(object):
    def __init__(self, name, description, unit_amount, quantity, customerID):
        self.name = name
        self.description = description
        self.unit_amount = unit_amount
        self.quantity = quantity
        self.customerID = customerID

class GuestStripeInformation(object):
    def __init__(self, name, description, unit_amount, quantity):
        self.name = name
        self.description = description
        self.unit_amount = unit_amount
        self.quantity = quantity

class StripeInformationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    unit_amount = serializers.IntegerField()
    quantity = serializers.IntegerField()
    customerID = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return StripeInformation(**validated_data)
    
class GuestStripeInformationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    unit_amount = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def create(self, validated_data):
        return GuestStripeInformation(**validated_data)