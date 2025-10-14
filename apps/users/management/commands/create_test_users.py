from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.users.models import User

users = [
    {
        "first_name": "Dennis",
        "last_name": "Paz",
        "email": "dppazlopez@gmail.com",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "first_name": "Djalma",
        "last_name": "Paz",
        "email": "djalmapaz@gmail.com",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "first_name": "Narcisa",
        "last_name": "Lopez",
        "email": "elastomeros.ec@gmail.com",
        "is_staff": True,
        "is_superuser": True,
    },
]
password = "12345"  # noqa: S105


class Command(BaseCommand):
    help = "Create or update test users in the database."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for data in users:
            email = data["email"]
            user, created = User.objects.update_or_create(
                email=email,
                defaults={**data},
            )
            if created:
                user.set_password(password)
                user.save()
                action = "Created"
                style = self.style.SUCCESS
            else:
                action = "Updated"
                style = self.style.WARNING
            EmailAddress.objects.update_or_create(
                user=user,
                email=email,
                defaults={"primary": True, "verified": True},
            )
            self.stdout.write(style(f"{action} user: {user}"))
