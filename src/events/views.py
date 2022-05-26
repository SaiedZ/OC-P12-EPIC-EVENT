import logging

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

logger = logging.getLogger('custom_logger')


class EventViewSet(viewsets.ModelViewSet):
    """ModelViewSet for Event."""

    serializer_class = EventSerializer
    permission_classes = [HasEventPermission & ClosedEventsToReadOnly]
    filter_fields = [
        'support_contact',
        'contract',
        'date_created',
        'date_updated',
        'status',
        'attendees',
        'event_date',
        'notes',
    ]

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

    def check_permissions(self, request):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                logger.warning(f"Unauthorized user ` {request.user} ` "
                               f"tried to access {request.path} "
                               f"using  {request.method=}")
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def check_object_permissions(self, request, obj):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                logger.warning(f"Unauthorized user ` {request.user} ` "
                               f"tried to access {request.path} "
                               f"using  {request.method=}")
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )


class EventStatusViewSet(viewsets.ModelViewSet):

    serializer_class = EventStatusSerializer
    permission_classes = [HasEventStatusPermission]
    queryset = models.EventStatus.objects.all()

    # Raising error message for unallwoed methods
    def partial_update(self, request, pk=None):
        return self._get_response_object("Partial update")

    def update(self, request, pk=None):
        return self._get_response_object("Update")

    def retrieve(self, request, pk=None):
        return self._get_response_object("Retrieve")

    def _get_response_object(self, method_name):
        response = {
            'message': f'{method_name} function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
