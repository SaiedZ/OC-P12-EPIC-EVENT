"""
Test custom Django management commands.
"""
from django.test import TestCase
from django.core.management import call_command
from events.management.commands.init_event_status import EVENT_STATUS

from events.models import EventStatus


class CommandTests(TestCase):
    """Test commands."""

    def test_init_eventstatus(self):

        call_command('init_event_status')

        for status in EVENT_STATUS:
            self.assertTrue(
                EventStatus.objects.filter(name=status['name']).exists()
            )
