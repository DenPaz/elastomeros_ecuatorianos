from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand

from apps.users.models import User

data = [
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

    def handle(self, *args, **kwargs):
        for entry in data:
            email = entry["email"]
            user, created = User.objects.update_or_create(
                email=email,
                defaults={**entry},
            )
            if created:
                user.set_password(password)
                user.save()
            EmailAddress.objects.update_or_create(
                user=user,
                email=email,
                defaults={"primary": True, "verified": True},
            )
            action = "Created" if created else "Updated"
            style = self.style.SUCCESS if created else self.style.WARNING
            self.stdout.write(style(f"{action} user: {user}"))
