from django.core.management import BaseCommand
from django.db import IntegrityError, transaction
from django.utils.text import slugify
from django_rbac_boiler_plate.models import Permission


class Command(BaseCommand):
    """
    Populate Permission
    """

    PERMISSION = (
        'Create User',
        'View User',
        'Delete User',
        'Update User'
    )

    def handle(self, *args, **options):
        self.stdout.write('Populating Permission...')

        try:
            with transaction.atomic():
                for permission in self.PERMISSION:
                    slug = slugify('_'.join([permission]), allow_unicode=False)
                    Permission.objects.create(name=permission, slug=slug)
        except IntegrityError as _:
            self.stderr.write('Duplicate Permission error')

        self.stdout.write(self.style.SUCCESS('Permission Successfully Populated!'))