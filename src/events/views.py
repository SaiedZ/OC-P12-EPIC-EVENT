from rest_framework import viewsets

from events import models
from events.serializers import EventSerializer, EventStatusSerializer


class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        return models.Event.objects.all()


class EventStatusViewSet(viewsets.ModelViewSet):

    serializer_class = EventStatusSerializer

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        return models.EventStatus.objects.all()
