from django.core.management.base import BaseCommand

from apps.products.models import Attribute
from apps.products.models import AttributeValue

data = [
    {
        "attribute_name": "Color de guantes",
        "value": "Amarillo",
        "sort_order": 0,
        "is_active": True,
    },
    {
        "attribute_name": "Color de guantes",
        "value": "Bicolor",
        "sort_order": 1,
        "is_active": True,
    },
    {
        "attribute_name": "Tamaño de guantes",
        "value": "7",
        "sort_order": 0,
        "is_active": True,
    },
    {
        "attribute_name": "Tamaño de guantes",
        "value": "7.5",
        "sort_order": 1,
        "is_active": True,
    },
    {
        "attribute_name": "Tamaño de guantes",
        "value": "8",
        "sort_order": 2,
        "is_active": True,
    },
    {
        "attribute_name": "Tamaño de guantes",
        "value": "8.5",
        "sort_order": 3,
        "is_active": True,
    },
    {
        "attribute_name": "Tamaño de guantes",
        "value": "9",
        "sort_order": 4,
        "is_active": True,
    },
    {
        "attribute_name": "Volumen del recipiente",
        "value": "1 Galón",
        "sort_order": 0,
        "is_active": True,
    },
    {
        "attribute_name": "Volumen del recipiente",
        "value": "5 Galones",
        "sort_order": 1,
        "is_active": True,
    },
]


class Command(BaseCommand):
    help = "Create or update product attribute values in the database."

    def handle(self, *args, **kwargs):
        for entry in data:
            attribute_name = entry.pop("attribute_name")
            attribute = Attribute.objects.get(name=attribute_name)
            lookup = {
                "attribute": attribute,
                "value": entry["value"],
            }
            defaults = {k: v for k, v in entry.items() if k not in lookup}
            obj, created = AttributeValue.objects.update_or_create(
                **lookup,
                defaults=defaults,
            )
            action = "Created" if created else "Updated"
            style = self.style.SUCCESS if created else self.style.WARNING
            self.stdout.write(style(f"{action} attribute value: {obj}"))
