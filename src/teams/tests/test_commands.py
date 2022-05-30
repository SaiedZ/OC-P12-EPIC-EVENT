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

        teams_number = Team.objects.all().count()
        self.assertEqual(len(TEAMS), teams_number)

        for id, team in enumerate(TEAMS, start=1):
            self.assertEqual(team['name'], Team.objects.get(id=id).name)
