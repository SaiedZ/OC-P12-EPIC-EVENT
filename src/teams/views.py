from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from . import models
from . import permissions as team_permissions
from .serializers import CRMUserSerializer, TeamSerializer


class CRMUserViewSet(viewsets.ModelViewSet):
    """ModelViewSet for CRMUser."""

    serializer_class = CRMUserSerializer
    permission_classes = [
        team_permissions.IsAuthenticatedAndSuperUserOrFromManagement
    ]

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        return models.CRMUser.objects.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context["view_action"] = self.action
        return context


class TeamViewSet(viewsets.ModelViewSet):
    """ModelViewSet for Team."""

    serializer_class = TeamSerializer
    queryset = models.Team.objects.all()
    permission_classes = [
        team_permissions.IsAuthenticatedAndSuperUserOrManagerForSafeMethods]

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
