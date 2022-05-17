from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import PasswordField

from .models import CRMUser, Team


class TeamSerializer(serializers.ModelSerializer):
    """Model serializer for Team."""

    class Meta:
        model = Team
        fields = ('name',)


class CRMUserSerializer(serializers.ModelSerializer):
    """Serializer for CRM users."""

    class Meta:
        model = CRMUser
        fields = ('email', 'username', 'first_name',
                  'last_name', 'phone', 'mobile')


class CreateCRMUserSerializer(serializers.ModelSerializer):
    """Serializer to create CRM users."""

    password = PasswordField()

    class Meta:
        model = CRMUser
        fields = ['id', 'email', 'username', 'first_name',
                  'password', 'last_name', 'phone', 'mobile',
                  'is_staff', 'is_active', 'is_superuser', 'team']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, password):
        if validate_password(password) is None:
            # return make_password(password)
            return password

    def create(self, validated_data):
        """ Create and return new user"""

        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
