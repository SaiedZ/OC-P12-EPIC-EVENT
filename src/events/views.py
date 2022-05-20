from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from events import models
from events.serializers import EventSerializer, EventStatusSerializer


class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer

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


class EventStatusViewSet(viewsets.ModelViewSet):

    serializer_class = EventStatusSerializer

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
