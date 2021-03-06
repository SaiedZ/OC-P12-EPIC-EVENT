"""
Views for events app.
"""

import logging

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from events import models
from events.serializers import EventSerializer, EventStatusSerializer
from events.permissions import (
    HasEventStatusPermission,
    HasEventPermission,
    ClosedEventsToReadOnly
)
from events.filters import EventFilter

logger = logging.getLogger('custom_logger')


class EventViewSet(viewsets.ModelViewSet):
    """ModelViewSet for Event."""

    serializer_class = EventSerializer
    permission_classes = [HasEventPermission & ClosedEventsToReadOnly]
    filterset_class = EventFilter

    def get_queryset(self):
        """
        Get the list of items for this view.

        Additionnal filter was added make distinction between ongoing
        and finished events.
        """
        if 'status' in self.request.query_params:
            return models.Event.objects.filter(
                status__name=self.request.query_params['status'])
        return models.Event.objects.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context["view_action"] = self.action
        return context

    def partial_update(self, request, pk=None):
        return self._get_response_object("Partial update")

    def _get_response_object(self, method_name):
        response = {
            'message': f'{method_name} function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'])
    def close_event(self, request, pk=None):
        """
        Custum method to close and event.

        Raise error if the event is already closed.
        """
        event = self.get_object()

        if event.status.name == "ongoing":
            status_finished = models.EventStatus.objects.filter(
                name="finished")[0]
            event.status = status_finished
            event.save(update_fields=['status'])
            content = {'message': 'Event have been closed successfully.'}
            return Response(content, status=status.HTTP_201_CREATED)

        content = {"message": "Event is already closed."}
        return Response(content, status=status.HTTP_409_CONFLICT)


class EventStatusViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """ModelViewSet for EventStatus model.

    A viewset that provides `create()`, `destroy()` and `list()` actions.
    """

    serializer_class = EventStatusSerializer
    permission_classes = [HasEventStatusPermission]
    queryset = models.EventStatus.objects.all()
