"""
Tests for the teams views.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from teams.models import Team
from teams.serializers import CRMUserSerializer, TeamSerializer


USER_LIST_URL = reverse("teams:user-list")


def create_user(**params):
    """Create and return a crm user."""
    defaults = {
        "email": "user@example.com",
        "username": "user",
        "password": "test12345",
        "first_name": "John",
        "last_name": "Doe",
        "mobile": "+9999999999",
    }
    defaults.update(params)

    return get_user_model().objects.create_user(**defaults)


class PublicUserAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(USER_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.management_team = Team.objects.create(name="management")
        self.admin_user = create_user(
            is_superuser=True,
            email="admin@example.com",
        )
        self.client.force_authenticate(self.admin_user)
        self.context_list = {"view_action": "list"}
        self.context_retrieve = {"view_action": "retrieve"}
        self.context_create = {"view_action": "create"}

    def test_list_users(self):
        """Test retrieving a list of users."""
        create_user(username="toto", email="toto@example.com")
        create_user(username="dodo", email="dodo@example.com")

        res = self.client.get(USER_LIST_URL)

        users = get_user_model().objects.all()
        serializer = CRMUserSerializer(
            users,
            context=self.context_list,
            many=True
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_detail_user(self):
        """Test get a user's detail."""
        url = reverse("teams:user-detail", args=[self.admin_user.id])
        res = self.client.get(url)

        serializer = CRMUserSerializer(
            self.admin_user,
            context=self.context_retrieve
        )

        self.assertEqual(res.data, serializer.data)

    def test_sale_or_supporthave_not_access_users(self):
        """Test permissions for access the users list."""

        sale_team = Team.objects.create(name="Sale")
        support_team = Team.objects.create(name="support")
        sale_user = create_user(
            team=sale_team, username="sale_u", email="toto@example.com"
        )
        support_user = create_user(
            team=support_team, username="supp_u", email="sup@example.com"
        )

        self.client.force_authenticate(sale_user)
        res = self.client.get(USER_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(support_user)
        res = self.client.get(USER_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
