from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from events import models
from events.serializers import EventSerializer, EventStatusSerializer
from events.permissions import HasEventStatusPermission, HasEventPermission


class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer
    permission_classes = [HasEventPermission]

    def get_queryset(self):
        """
        Get the list of items for this view.
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


class EventStatusViewSet(viewsets.ModelViewSet):

    serializer_class = EventStatusSerializer
    permission_classes = [HasEventStatusPermission]

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        return models.EventStatus.objects.all()

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
