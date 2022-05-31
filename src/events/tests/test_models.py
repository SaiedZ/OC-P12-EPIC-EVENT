"""
Tests for the contracts models.
"""

from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from clients.models import Client
from contracts.models import Contract
from events.models import Event, EventStatus


class ContractModelTest(TestCase):

    def setUp(self):

        self.client = Client.objects.create(
            first_name='first_name',
            last_name='last_name',
            email='client@example.com',
            phone='+9999999999',
            compagny_name='Sample CO.',
        )
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            username="sale_user",
            password="test12345",
            first_name="John",
            last_name="Doe",
            mobile="+9999999999",
        )

        self.test_date = datetime.strptime(
            "2022/12/01 12:00:00",
            '%Y/%m/%d %H:%M:%S',
        )

        self.contract = Contract.objects.create(
            sales_contact=self.user,
            client=self.client,
            amount=12345.6,
            payment_due=self.test_date,
        )

    def test_create_event_status(self):
        """Test creating a event statut is successful."""
        event_status = self._create_event_statut()
        self.assertEqual(event_status.name, "ongoing")

    def test_create_event(self):
        """Test creating a event is successful."""
        event_status = self._create_event_statut()
        event = Event.objects.create(
            contract=self.contract,
            support_contact=self.user,
            status=event_status,
            attendees=1000,
            event_date=self.test_date,
            notes="test creating event !"
        )

        self.assertEqual(
            str(event.contract),
            f"{self.contract.client} - {self.contract.sales_contact}"
        )

    def _create_event_statut(self):
        """Utils function for creating EventStatus."""

        return EventStatus.objects.create(name="ongoing")
