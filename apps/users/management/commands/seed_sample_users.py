from django.core.management.base import BaseCommand
from django.db import transaction

from apps.users.models import User
from apps.users.tests.factories import UserFactory


class Command(BaseCommand):
    help = "Seed the database with sample users."

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=50)
        parser.add_argument("--clear", action="store_true")

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if kwargs["clear"]:
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS("Cleared existing user data."))

        for _ in range(kwargs["users"]):
            UserFactory()
        self.stdout.write(self.style.SUCCESS("Successfully seeded user data."))
