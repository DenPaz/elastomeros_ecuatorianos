from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update the Site domain and name based on settings"

    def handle(self, *args, **options):
        site = Site.objects.get_current()
        site.name = "Localhost" if settings.DEBUG else settings.SITE_NAME
        site.domain = "localhost:8000" if settings.DEBUG else settings.SITE_DOMAIN
        site.save()
        self.stdout.write(self.style.SUCCESS(f"Site updated: {site.domain}"))
