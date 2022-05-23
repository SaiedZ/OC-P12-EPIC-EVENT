
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    """A serializer for client objects."""

    class Meta:
        model = Client
        fields = ("id", "compagny_name", "first_name",
                  "last_name", "email", "phone", "mobile",
                  "potential", "date_created", "date_updated")
        extra_kwargs = {
            'potential': {'read_only': True},
        }

    def validate(self, data):

        phone = data.get('phone')
        mobile = data.get('mobile')

        if phone is None and mobile is None:
            raise serializers.ValidationError(
                _("Client must have a phone or mobile number.")
            )
        return data
