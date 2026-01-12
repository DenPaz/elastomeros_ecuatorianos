from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand

from apps.users.models import User

test_users = [
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
    help = "Create or update test users in the database"

    def handle(self, *args, **kwargs):
        for test_user in test_users:
            user, created = User.objects.update_or_create(
                email=test_user["email"],
                defaults={
                    "first_name": test_user["first_name"],
                    "last_name": test_user["last_name"],
                    "is_staff": test_user["is_staff"],
                    "is_superuser": test_user["is_superuser"],
                },
            )
            user.set_password(password)
            user.save()

            EmailAddress.objects.update_or_create(
                user=user,
                email=user.email,
                defaults={"verified": True, "primary": True},
            )

            action = "Created" if created else "Updated"
            style = self.style.SUCCESS if created else self.style.WARNING
            self.stdout.write(style(f"{action} user: {user}"))
