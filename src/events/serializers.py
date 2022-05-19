from rest_framework import serializers

from events.models import EventStatus, Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'contract', 'support_contact', 'status', 'attendees',
                  'event_date', 'notes', 'date_created', 'date_updated']


class EventStatus(serializers.ModelSerializer):

    class Meta:
        model = EventStatus
        fields = ['id', 'name']
