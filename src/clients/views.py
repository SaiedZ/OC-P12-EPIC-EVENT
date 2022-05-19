from rest_framework import viewsets

from clients import models
from clients.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):

    serializer_class = ClientSerializer

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        return models.Client.objects.all()
