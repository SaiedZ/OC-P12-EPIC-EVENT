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

    def validate(self, data):
        support_contact = data.get("sales_contact")
        if support_contact.team is None:
            raise serializers.ValidationError(
                _("Sales contact must be par of the `Support` team.")
            )
        elif support_contact.team.name != "Support":
            raise serializers.ValidationError(
                _("Sales contact must be par of the `Support` team.")
            )
        return data


class EventStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventStatus
        fields = ['id', 'name']
