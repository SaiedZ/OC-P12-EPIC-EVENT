from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from contracts import models
from contracts.serializers import ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):

    serializer_class = ContractSerializer

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        return models.Contract.objects.all()

    @action(detail=True, methods=['get'])
    def sign_contract(self, request, pk=None):
        contract = self.get_object()
        if not contract.status:
            contract.status = True
            contract.save()
            content = {'message': 'Contract signed.'}
            return Response(content, status=status.HTTP_201_CREATED)
        content = {"message": "Contract already signed."}
        return Response(content, status=status.HTTP_409_CONFLICT)
