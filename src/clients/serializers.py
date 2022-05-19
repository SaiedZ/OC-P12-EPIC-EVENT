from rest_framework import serializers

from clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    """A serializer for client objects."""

    class Meta:
        model = Client
        fields = ("compagny_name", "first_name", "last_name", "email",
                  "phone", "mobile", "date_created", "date_updated")
