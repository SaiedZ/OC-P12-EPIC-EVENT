from rest_framework import viewsets
from rest_framework import filters

from clients import models
from clients.serializers import ClientSerializer
from clients.permissions import IsManager, HasClientPermissions


class ClientViewSet(viewsets.ModelViewSet):

    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsManager | HasClientPermissions]
    search_fields = ['potential']

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        if 'potential' in self.request.query_params:
            if self.request.query_params['potential'] == "true":
                return models.Client.objects.filter(potential=True)
            elif self.request.query_params['potential'] == "false":
                return models.Client.objects.filter(potential=False)
        return models.Client.objects.all()
