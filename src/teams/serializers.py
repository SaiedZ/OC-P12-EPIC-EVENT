from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import PasswordField

from .models import CRMUser, Team


class TeamSerializer(serializers.ModelSerializer):
    """Model serializer for Team."""

    class Meta:
        model = Team
        fields = ('id', 'name')


class CRMUserSerializer(serializers.ModelSerializer):
    """Serializer for CRM users."""

    def __init__(self, *args, **kwargs):
        """Initialize and if the view action is `list` or `retrieve`
        the team field will be set to `SerializerMethodField`.
        
        This will give the `name` of the team in addition to the id. 
        """
        super().__init__(*args, **kwargs)
        if self.context['view_action'] in ['retrieve', 'list']:
            self.fields['team'] = serializers.SerializerMethodField()

    password = PasswordField()

    class Meta:
        model = CRMUser
        fields = ['id', 'email', 'username', 'first_name',
                  'password', 'last_name', 'phone', 'mobile',
                  'is_staff', 'is_active', 'is_superuser', 'team']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
        }

    def get_team(self, instance):
        if instance.team:
            queryset = instance.team
            serializer = TeamSerializer(queryset)
            return serializer.data

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
