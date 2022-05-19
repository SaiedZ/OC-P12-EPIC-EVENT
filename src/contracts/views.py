from rest_framework import viewsets

from contracts import models
from contracts.serializers import ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):

    serializer_class = ContractSerializer

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        return models.Contract.objects.all()
