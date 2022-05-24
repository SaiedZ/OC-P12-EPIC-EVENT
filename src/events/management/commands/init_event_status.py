from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from events.models import EventStatus

CRMUser = get_user_model()

EVENT_STATUS = [
    {'name': 'ongoing'},
    {'name': 'finished'}
]


class Command(BaseCommand):

    help = ('Initialize the team objects by creating: '
            'Management and Sale and Support teams'
            )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        for data_status in EVENT_STATUS:
            if not EventStatus.objects.filter(
                    name=data_status['name']).exists():
                EventStatus.objects.create(name=data_status['name'])

        self.stdout.write(self.style.SUCCESS("All Done !"))
