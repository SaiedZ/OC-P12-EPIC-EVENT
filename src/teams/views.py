from rest_framework import generics, permissions
from rest_framework import viewsets

from . import models
from .serializers import CRMUserSerializer


class CreateUserViewSet(generics.CreateAPIView):
    """
    Handels the creatinon of new CRM users

    This view is only accessible for ?????????????????????????????????????
    """

    serializer_class = CRMUserSerializer
    queryset = models.CRMUser.objects.all()
    permission_classes = [~permissions.IsAuthenticated]


class CRMUserViewSet(viewsets.ModelViewSet):

    serializer_class = CRMUserSerializer

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