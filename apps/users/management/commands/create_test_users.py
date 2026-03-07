from django.core.management.base import BaseCommand
from django.db import transaction

from apps.users.models import User
from apps.users.tests.factories import UserFactory


class Command(BaseCommand):
    help = "Create test users for development and testing purposes."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=50)
        parser.add_argument("--clean", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        count = options["count"]
        clean = options["clean"]

        if clean:
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS("Deleted existing test users."))

        for _ in range(count):
            UserFactory.create()
        self.stdout.write(self.style.SUCCESS(f"Created {count} test users."))
