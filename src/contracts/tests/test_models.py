"""
Tests for the contracts models.
"""

from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from teams.models import Team
from clients.models import Client
from contracts.models import Contract


class ContractModelTest(TestCase):

    def test_create_client(self):
        """Test creating a contract is successful."""

        client = Client.objects.create(
            first_name='first_name',
            last_name='last_name',
            email='client@example.com',
            phone='+9999999999',
            compagny_name='Sample CO.',
        )
        sale_user = get_user_model().objects.create_user(
            email="user@example.com",
            username="sale_user",
            password="test12345",
            first_name="John",
            last_name="Doe",
            mobile="+9999999999",
        )

        payment_due = datetime.strptime(
            "2022/12/01 12:00:00",
            '%Y/%m/%d %H:%M:%S',
        )

        contract = Contract.objects.create(
            sales_contact=sale_user,
            client=client,
            amount=12345.6,
            payment_due=payment_due,
        )
        self.assertEqual(
            str(contract),
            f"{contract.client} - {contract.sales_contact}"
        )
