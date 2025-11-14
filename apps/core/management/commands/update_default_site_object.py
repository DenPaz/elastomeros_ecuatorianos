from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update the default Site object with settings values."

    def handle(self, *args, **kwargs):
        site = Site.objects.get(id=settings.SITE_ID)
        site.name = "Localhost" if settings.DEBUG else settings.SITE_NAME
        site.domain = "localhost:8000" if settings.DEBUG else settings.SITE_DOMAIN
        site.save()
        self.stdout.write(self.style.SUCCESS(f"Site object updated: {site.domain}"))
