from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from contracts.models import Contract
from teams.serializers import CRMUserSerializer
from clients.serializers import ClientSerializer


class ContractSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        """Initialize and if the view action is `list` or `retrieve`
        the contract field will be set to `ContractSerializer`.

        This will give extras informations about the contract.
        """
        super().__init__(*args, **kwargs)
        if self.context["view_action"] == "retrieve":
            self.fields["client"] = ClientSerializer()
            self.fields["sales_contact"] = CRMUserSerializer(
                context=self.context)
        if self.context["view_action"] == "list":
            self.fields["client"] = serializers.StringRelatedField()
            self.fields["sales_contact"] = serializers.StringRelatedField()

    class Meta:
        model = Contract
        fields = [
            "id",
            "sales_contact",
            "client",
            "status",
            "amount",
            "payment_due",
            "date_created",
            "date_updated",
        ]
        extra_kwargs = {
            "status": {"read_only": True},
        }

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["date_created"] = instance.date_created.strftime(
            "%H:%M:%S %d-%m-%Y")
        response["date_updated"] = instance.date_updated.strftime(
            "%H:%M:%S %d-%m-%Y")
        return response

    def validate_sales_contact(self, sales_contact):
        """sales_contact must be part of the Sale Team."""
        if sales_contact.team is None:
            raise serializers.ValidationError(
                _("Sales contact must be par of the `Sale` team.")
            )
        elif sales_contact.team.name != "Sale":
            raise serializers.ValidationError(
                _("Sales contact must be par of the `Sale` team.")
            )
        return sales_contact
