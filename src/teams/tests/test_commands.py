"""
Test custom Django management commands.
"""
from django.test import TestCase
from django.core.management import call_command
from teams.management.commands.init_teams import TEAMS

from teams.models import Team


class CommandTests(TestCase):
    """Test commands."""

    def test_init_teams(self):

        call_command('init_teams')

        for team in TEAMS:
            self.assertTrue(Team.objects.filter(name=team['name']).exists())
