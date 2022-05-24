from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from teams.models import Team

CRMUser = get_user_model()

TEAMS = [
    {'name': 'Management'},
    {'name': 'Sale'},
    {'name': 'Support'}
]


class Command(BaseCommand):

    help = 'Initialize the team objects by creating: Management and Sale and Support teams'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        for data_team in TEAMS:
            if not Team.objects.filter(name=data_team['name']).exists():
                Team.objects.create(name=data_team['name'])

        self.stdout.write(self.style.SUCCESS("All Done !"))
