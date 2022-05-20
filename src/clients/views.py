from rest_framework import viewsets
from rest_framework import filters

from clients import models
from clients.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):

    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['potential']

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        return models.Client.objects.all()
