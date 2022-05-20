from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django.dispatch import receiver
from django.db.models.signals import post_save

from contracts.serializers import ContractSerializer
from contracts import models as contracts_models


class ContractViewSet(viewsets.ModelViewSet):

    serializer_class = ContractSerializer

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        return contracts_models.Contract.objects.all()

    @action(detail=True, methods=['get'])
    def sign_contract(self, request, pk=None):
        contract = self.get_object()
        if not contract.status:
            contract.status = True
            contract.save(update_fields=['status'])
            content = {'message': 'Contract signed.'}
            return Response(content, status=status.HTTP_201_CREATED)
        content = {"message": "Contract already signed."}
        return Response(content, status=status.HTTP_409_CONFLICT)


@receiver(post_save, sender=contracts_models.Contract)
def update_client_from_potential_to_existant(sender, instance, *args, **kwargs):
    if kwargs['update_fields'] is not None and 'status' in kwargs['update_fields']:
        instance.client.potential = False
        instance.client.save(update_fields=['potential'])
