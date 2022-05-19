from rest_framework import serializers

from contracts.models import Contract


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['sales_contact', 'client', 'status', 'amount',
                  'payment_due', 'date_created', 'date_updated']
