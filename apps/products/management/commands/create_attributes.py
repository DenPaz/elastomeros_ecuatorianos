from django.core.management.base import BaseCommand

from apps.products.models import Attribute

data = [
    {
        "name": "Color de guantes",
        "description": "Atributo que define los colores disponibles para los guantes.",
        "is_active": True,
    },
    {
        "name": "Tamaño de guantes",
        "description": "Atributo que define los tamaños disponibles para los guantes.",
        "is_active": True,
    },
    {
        "name": "Volumen del recipiente",
        "description": (
            "Atributo que define los volúmenes disponibles para los recipientes "
            "de líquidos."
        ),
        "is_active": True,
    },
]


class Command(BaseCommand):
    help = "Create or update product attributes in the database."

    def handle(self, *args, **kwargs):
        for entry in data:
            lookup = {
                "name": entry["name"],
            }
            defaults = {k: v for k, v in entry.items() if k not in lookup}
            obj, created = Attribute.objects.update_or_create(
                **lookup,
                defaults=defaults,
            )
            action = "Created" if created else "Updated"
            style = self.style.SUCCESS if created else self.style.WARNING
            self.stdout.write(style(f"{action} attribute: {obj}"))
