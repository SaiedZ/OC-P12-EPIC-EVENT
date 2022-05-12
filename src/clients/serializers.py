from rest_framework import serializers
from clients.models import Client


class ClientListSerializer(serializers.ModelSerializer):
    """A serializer for client objects.

    used for list serialization.
    """

    class Meta:
        model = Client
        fields = ("compagny_name", "first_name", "last_name")


class ClientDetailSerializer(serializers.ModelSerializer):
    """A serializer for client objects.

    used for detail serialization.
    """

    class Meta:
        model = Client
        fields = ("compagny_name", "first_name", "last_name", "email",
                  "phone", "mobile", "date_created", "date_updated")
