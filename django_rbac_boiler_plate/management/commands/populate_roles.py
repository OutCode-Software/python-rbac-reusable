from django.core.management import BaseCommand
from django.db import IntegrityError, transaction
from django_rbac_boiler_plate.models import Role


class Command(BaseCommand):
    """
    Populate Roles
    """

    ROLES = (
        'SuperAdmin',
        'Admin'
        'User'
    )

    def handle(self, *args, **options):
        self.stdout.write('Populating Roles...')
        
        try:
            with transaction.atomic():
                Role.objects.bulk_create([Role(name=role) for role in self.ROLES])
        except IntegrityError as _:
            self.stderr.write('Duplicate Role error')

        self.stdout.write(self.style.SUCCESS('Roles Successfully Populated!'))
