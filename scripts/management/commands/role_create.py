from django.core.management import BaseCommand

from access_control.models import Role

ROLE_TYPES = [
    'Owner',
    'Manager',
    'Developer'
]


class Command(BaseCommand):
    help = "Add Roles to database"

    def handle(self, *args, **options):
        for _,role in enumerate(ROLE_TYPES):
            Role.objects.create(name=role, role=_+1)
