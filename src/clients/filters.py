
from django_filters import rest_framework as filters
from .models import Client


class ClientFilter(filters.FilterSet):
    """
    Client filter for API search.
    """
    class Meta:
        model = Client
        fields = {
            'phone': ['icontains', 'iexact'],
            'mobile': ['icontains', 'iexact'],
            'email': ['icontains', 'iexact'],
            'first_name': ['icontains', 'iexact'],
            'last_name': ['icontains', 'iexact'],
            'compagny_name': ['icontains', 'iexact'],
        }
