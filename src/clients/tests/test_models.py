"""
Tests for the clients models.
"""

from django.test import TestCase

from clients.models import Client


class ClientModelTest(TestCase):

    def test_create_client(self):
        """Test creating a Client is successful."""
        client = Client.objects.create(
            first_name='first_name',
            last_name='last_name',
            email='client@example.com',
            phone='+9999999999',
            compagny_name='Sample CO.',
        )

        self.assertEqual(str(client), client.compagny_name.capitalize())
