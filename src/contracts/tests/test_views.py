"""
Tests for the contracts views.
"""

from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from teams.models import Team
from clients.models import Client
from contracts.models import Contract
from contracts.serializers import ContractSerializer


CONTRACT_LIST_URL = reverse("contracts:contract-list")


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
        res = self.client.get(CONTRACT_LIST_URL)

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
        self.date_test = datetime.strptime(
            "2024/12/01 12:00:00",
            '%Y/%m/%d %H:%M:%S',
        )

    def test_list_contracts(self):
        """Test retrieving a list of contracts."""
        client = create_client(
            compagny_name="client1",
            email="Client1@example.com"
        )

        Contract.objects.create(
            sales_contact=self.Sale_user,
            client=client,
            amount=12345.6,
            payment_due=self.date_test,
        )

        res = self.client.get(CONTRACT_LIST_URL)

        contracts = Contract.objects.all()
        serializer = ContractSerializer(
            contracts,
            context=self.context_list,
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_detail_contract(self):
        """Test get a contract's detail."""

        client = create_client(
            compagny_name="client1",
            email="Client1@example.com"
        )

        contract_test = Contract.objects.create(
            sales_contact=self.Sale_user,
            client=client,
            amount=12345.6,
            payment_due=self.date_test,
        )

        url = reverse("contracts:contract-detail", args=[contract_test.id])
        res = self.client.get(url)

        serializer = ContractSerializer(
            contract_test,
            context=self.context_retrieve
        )

        self.assertEqual(res.data, serializer.data)

    def test_delete_contract(self):
        """Test delete."""
        client = create_client(
            compagny_name="client1",
            email="Client1@example.com"
        )

        contract_test = Contract.objects.create(
            sales_contact=self.Sale_user,
            client=client,
            amount=12345.6,
            payment_due=self.date_test,
        )
        url = reverse("contracts:contract-detail", args=[contract_test.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=contract_test.id).exists())
