from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django.dispatch import receiver
from django.db.models.signals import post_save

from contracts.serializers import ContractSerializer
from contracts import models as contracts_models
from contracts.permissions import ContractPermissionSafeAndPost


class ContractViewSet(viewsets.ModelViewSet):

    serializer_class = ContractSerializer
    permission_classes = [ContractPermissionSafeAndPost]

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        if 'status' in self.request.query_params:
            if self.request.query_params['status'].capitalize() == "True":
                return contracts_models.Contract.objects.filter(status=True)
            if self.request.query_params['status'].capitalize() == "False":
                return contracts_models.Contract.objects.filter(status=False)
            return contracts_models.Contract.objects.none()
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

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context["view_action"] = self.action
        return context


@receiver(post_save, sender=contracts_models.Contract)
def update_client_from_potential_to_existant(sender, instance, *args, **kwargs):
    if kwargs['update_fields'] is not None and 'status' in kwargs['update_fields']:
        instance.client.potential = False
        instance.client.save(update_fields=['potential'])
