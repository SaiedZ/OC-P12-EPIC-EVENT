"""
Tests for the Django admin modifications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
            username='admin',
            first_name='admin',
            last_name='admin',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            username='Test User',
            first_name='test_user',
            last_name='test_user',
        )

    def test_users_lists(self):
        """Test that users are listed on page."""
        url = reverse('admin:teams_crmuser_changelist')
        res = self.client.get(url)

        self.assertContains(res, str(self.user))
        # self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:teams_crmuser_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:teams_crmuser_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
