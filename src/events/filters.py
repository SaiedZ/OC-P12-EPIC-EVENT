
from django_filters import rest_framework as filters
from .models import Event


class EventFilter(filters.FilterSet):
    """
    Event filter for API search.
    """
    class Meta:
        model = Event
        fields = {
            'support_contact__first_name': ['exact', 'icontains'],
            'support_contact__last_name': ['exact', 'icontains'],
            'support_contact__email': ['exact', 'icontains'],
            'contract__sales_contact__first_name': ['exact', 'icontains'],
            'contract__sales_contact__last_name': ['exact', 'icontains'],
            'contract__sales_contact__email': ['exact', 'icontains'],
            'date_created': ['exact', 'gte', 'lte'],
            'date_updated': ['exact', 'gte', 'lte'],
            'status__name': ['exact'],
            'attendees': ['exact', 'gte', 'lte'],
            'event_date': ['exact', 'gte', 'lte'],
            'notes': ['exact', 'icontains'],
        }
