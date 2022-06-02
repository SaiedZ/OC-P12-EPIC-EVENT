"""
Views for the user API.
"""

from django.contrib.auth import get_user_model

from rest_framework import mixins
from rest_framework import viewsets

from . import models
from . import permissions as team_permissions
from .serializers import CRMUserSerializer, TeamSerializer
from .filters import CRMUserFilter


class CRMUserViewSet(viewsets.ModelViewSet):
    """ModelViewSet for CRMUser."""

    serializer_class = CRMUserSerializer
    permission_classes = [
        team_permissions.IsSuperUserOrFromManagement
    ]
    filterset_class = CRMUserFilter

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        return get_user_model().objects.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context["view_action"] = self.action
        return context


class TeamViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """ModelViewSet for Team.

    A viewset that provides `create()`, `destroy()` and `list()` actions.
    """

    serializer_class = TeamSerializer
    queryset = models.Team.objects.all()
    permission_classes = [
        team_permissions.IsSuperUserOrManagerForSafeMethods]
