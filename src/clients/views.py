from rest_framework import viewsets

from clients import models
from clients.serializers import ClientSerializer
from clients.permissions import IsManager, HasClientPermissions
from clients.filters import ClientFilter


class ClientViewSet(viewsets.ModelViewSet):
    """ModelViewSet for Client model."""

    serializer_class = ClientSerializer
    permission_classes = [IsManager | HasClientPermissions]
    filter_class = ClientFilter

    def get_queryset(self):
        """
        Get the list of items for this view.

        A filter was added here to disctinct potential client
        from existing ones.
        """
        if 'potential' in self.request.query_params:
            if self.request.query_params['potential'].capitalize() == "True":
                return models.Client.objects.filter(potential=True)
            if self.request.query_params['potential'].capitalize() == "False":
                return models.Client.objects.filter(potential=False)
            return models.Client.objects.none()

        return models.Client.objects.all()
