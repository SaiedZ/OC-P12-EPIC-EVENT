from django_filters import rest_framework as filters
from .models import Contract


class ContractFilter(filters.FilterSet):
    """
    Contract filter for API search.
    """
    class Meta:
        model = Contract
        fields = {
            'client__last_name': ['exact', 'icontains'],
            'client__first_name': ['exact', 'icontains'],
            'client__compagny_name': ['exact', 'icontains'],
            'client__email': ['exact', 'icontains'],
            'date_created': ['exact', 'icontains', 'gte', 'lte'],
            'date_updated': ['exact', 'icontains', 'gte', 'lte'],
            'amount': ['exact', 'gte', 'lte']
        }
