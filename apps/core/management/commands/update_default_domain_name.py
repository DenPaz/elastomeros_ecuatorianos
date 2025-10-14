from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update the default site object with the proper domain name."

    def handle(self, *args, **kwargs):
        site = Site.objects.get(id=settings.SITE_ID)
        if settings.DEBUG:
            site.name = "Localhost"
            site.domain = "localhost:8000"
        else:
            site.name = "Elastómeros Ecuatorianos"
            site.domain = "elastomeros-ecuatorianos.ec"
        site.save()
        self.stdout.write(self.style.SUCCESS(f"Site updated to {site.domain}"))
