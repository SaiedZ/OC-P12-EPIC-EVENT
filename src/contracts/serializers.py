from rest_framework import serializers

from contracts.models import Contract


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['id', 'sales_contact', 'client', 'status',
                  'amount', 'payment_due', 'date_created', 'date_updated']
        extra_kwargs = {
            'status': {'read_only': True},
        }
