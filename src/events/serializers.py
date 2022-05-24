from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from events.models import EventStatus, Event
from contracts.serializers import ContractSerializer
from teams.serializers import CRMUserSerializer


class EventSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        """Initialize and if the view action is `list` or `retrieve`
        the contract field will be set to `ContractSerializer`.

        This will give extras informations about the contract.
        """
        super().__init__(*args, **kwargs)
        if self.context['view_action'] == 'retrieve':
            self.fields['contract'] = ContractSerializer(context=self.context)
            self.fields['support_contact'] = CRMUserSerializer(
                context=self.context)
        if self.context['view_action'] == 'list':
            self.fields['support_contact'] = serializers.StringRelatedField()
            self.fields['contract'] = serializers.StringRelatedField()

    client_name = serializers.CharField(read_only=True,
                                        source=str('contract.client'))

    class Meta:
        model = Event
        fields = ['id', 'contract', 'support_contact', 'client_name',
                  'status', 'attendees', 'event_date', 'notes',
                  'date_created', 'date_updated']
        extra_kwargs = {
            "status": {"read_only": True},
        }

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['contract'] = ContractSerializer(instance.contract).data
        response['status'] = instance.status.name.capitalize()
        response['event_date'] = instance.event_date.strftime(
            "%H:%M:%S %d-%m-%Y")
        response['date_created'] = instance.date_created.strftime(
            "%H:%M:%S %d-%m-%Y")
        response['date_updated'] = instance.date_updated.strftime(
            "%H:%M:%S %d-%m-%Y")
        return response

    def validate_contract(self, contract):
        """Contract must be signed."""
        if not contract.status:
            raise serializers.ValidationError(
                _("Contract must be signed before creating the event.")
            )
        return contract

    def validate_support_contact(self, support_contact):
        """support_contact must be part of the Support Team."""
        # sourcery skip: merge-duplicate-blocks, remove-redundant-if
        if support_contact.team is None:
            raise serializers.ValidationError(
                _("Sales contact must be par of the `Support` team.")
            )
        elif support_contact.team.name != "Support":
            raise serializers.ValidationError(
                _("Sales contact must be par of the `Support` team.")
            )
        return support_contact

    def create(self, validated_data):
        """Setting the status to ongoing when creating an event."""
        instance = super().create(validated_data)
        ongoing_status = EventStatus.objects.filter(name="ongoing")[0]
        instance.status = ongoing_status
        return instance

class EventStatusSerializer(serializers.ModelSerializer):
    """A Sseralizer for EventsStatus"""
    class Meta:
        model = EventStatus
        fields = ['id', 'name']
