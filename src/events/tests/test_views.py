"""
Tests for the events views.
"""

from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from teams.models import Team
from contracts.models import Contract
from clients.models import Client
from events.models import Event, EventStatus
from events.serializers import EventSerializer


EVENT_LIST_URL = reverse("events:event-list")


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


class PublicEventAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(EVENT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEventAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.sale_team = Team.objects.create(name="Sale")
        self.sale_user = create_user(
            team=self.sale_team,
            email="sale_user@example.com",
        )
        self.support_team = Team.objects.create(name="Support")
        self.support_user = create_user(
            team=self.support_team,
            email="support_user@example.com",
            username="sup_m",
        )
        self.client.force_authenticate(self.sale_user)
        self.context_list = {"view_action": "list"}
        self.context_retrieve = {"view_action": "retrieve"}
        self.context_create = {"view_action": "create"}
        self.context_destroy = {"view_action": "destroy"}
        self.date_test = datetime.strptime(
            "2024/12/01 12:00:00",
            '%Y/%m/%d %H:%M:%S',
        )

    def test_list_events(self):
        """Test retrieving a list of events."""

        event_status = self._create_event_statut()
        Event.objects.create(
            contract=self._create_contract(),
            support_contact=self.support_user,
            status=event_status,
            attendees=1000,
            event_date=self.date_test,
            notes="test creating event !"
        )

        res = self.client.get(EVENT_LIST_URL)

        events = Event.objects.all()
        serializer = EventSerializer(
            events,
            context=self.context_list,
            many=True
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_detail_event(self):
        """Test get an event's detail."""

        event_status = self._create_event_statut()
        event = Event.objects.create(
            contract=self._create_contract(),
            support_contact=self.support_user,
            status=event_status,
            attendees=1000,
            event_date=self.date_test,
            notes="test creating event !"
        )

        url = reverse("events:event-detail", args=[event.id])
        res = self.client.get(url)

        serializer = EventSerializer(
            event,
            context=self.context_retrieve
        )

        self.assertEqual(res.data, serializer.data)

    def test_delete_contract(self):
        """Test delete."""
        self.client.force_authenticate(self.support_user)
        event_status = self._create_event_statut()
        event = Event.objects.create(
            contract=self._create_contract(),
            support_contact=self.support_user,
            status=event_status,
            attendees=1000,
            event_date=self.date_test,
            notes="test creating event !"
        )
        url = reverse("events:event-detail", args=[event.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=event.id).exists())

    def _create_contract(self):
        client = create_client(
            compagny_name="client1",
            email="Client1@example.com"
        )

        return Contract.objects.create(
            sales_contact=self.sale_user,
            client=client,
            amount=12345.6,
            payment_due=self.date_test,
        )

    def _create_event_statut(self):
        """Utils function for creating EventStatus."""

        return EventStatus.objects.create(name="ongoing")