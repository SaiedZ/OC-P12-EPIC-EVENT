"""
Tests for the clients views.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from teams.models import Team
from clients.models import Client
from clients.serializers import ClientSerializer


CLIENT_LIST_URL = reverse("clients:client-list")


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


def create_client(**params):
    """Create and return a client."""
    defaults = {
        "email": "client@example.com",
        "compagny_name": "Compagny",
        "first_name": "John",
        "last_name": "Doe",
        "mobile": "+9999999999",
    }
    defaults.update(params)

    return Client.objects.create(**defaults)


class PublicClientAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(CLIENT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateClientAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.Sale_team = Team.objects.create(name="Sale")
        self.Sale_user = create_user(
            team=self.Sale_team,
            email="sale_user@example.com",
        )
        self.client.force_authenticate(self.Sale_user)
        self.context_list = {"view_action": "list"}
        self.context_retrieve = {"view_action": "retrieve"}
        self.context_create = {"view_action": "create"}
        self.context_destroy = {"view_action": "destroy"}

    def test_list_clients(self):
        """Test retrieving a list of clients."""
        create_client(compagny_name="client1", email="Client1@example.com")
        create_client(email="Client2@example.com")

        res = self.client.get(CLIENT_LIST_URL)

        clients = Client.objects.all()
        serializer = ClientSerializer(
            clients,
            context=self.context_list,
            many=True
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_detail_client(self):
        """Test get a client's detail."""
        client_test = create_client(compagny_name="c1", email="C1@example.com")
        url = reverse("clients:client-detail", args=[client_test.id])
        res = self.client.get(url)

        serializer = ClientSerializer(
            client_test,
            context=self.context_retrieve
        )

        self.assertEqual(res.data, serializer.data)

    def test_delete_client(self):
        """Test delete."""
        client_test = create_client(compagny_name="c1", email="C1@example.com")
        url = reverse("clients:client-detail", args=[client_test.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=client_test.id).exists())

    def test_update_client(self):
        """Test updating a client."""
        client_test = create_client(compagny_name="c1", email="C1@example.com")
        payload = {
            "email": "client@example.com",
            "compagny_name": "Compagny",
            "first_name": "John",
            "last_name": "Doe",
            "mobile": "+9999999999",
        }
        url = reverse("clients:client-detail", args=[client_test.id])
        self.client.put(url, payload)

        client_test.refresh_from_db()
        self.assertEqual(client_test.email, payload["email"])
