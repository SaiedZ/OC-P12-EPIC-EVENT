
from django_filters import rest_framework as filters
from .models import CRMUser


class CRMUserFilter(filters.FilterSet):
    """
    CRMUSer filter for API search.
    """
    class Meta:
        model = CRMUser
        fields = {
            'username': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'team__name': ['exact', 'icontains'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
        }
