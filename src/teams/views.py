from rest_framework import generics, permissions
from rest_framework import viewsets

from . import models
from .serializers import CreateCRMUserSerializer


class CreateUserViewSet(generics.CreateAPIView):
    """
    Handels the creatinon of new CRM users

    This view is only accessible for ?????????????????????????????????????
    """

    serializer_class = CreateCRMUserSerializer
    queryset = models.CRMUser.objects.all()
    permission_classes = [~permissions.IsAuthenticated]


class CRMUserViewSet(viewsets.ModelViewSet):

    serializer_class = CreateCRMUserSerializer

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        return models.CRMUser.objects.all()
