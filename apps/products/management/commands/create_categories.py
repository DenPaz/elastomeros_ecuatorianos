from django.core.management.base import BaseCommand

from apps.products.models import Category

data = [
    {
        "name": "Latex",
        "slug": "latex",
        "description": "Categoría para productos derivados del látex.",
        "is_active": True,
    },
    {
        "name": "Productos de caucho",
        "slug": "productos-de-caucho",
        "description": "Categoría para productos fabricados con caucho natural.",
        "is_active": True,
    },
]


class Command(BaseCommand):
    help = "Create or update product categories in the database."

    def handle(self, *args, **kwargs):
        for entry in data:
            lookup = {
                "name": entry["name"],
            }
            defaults = {k: v for k, v in entry.items() if k not in lookup}
            obj, created = Category.objects.update_or_create(
                **lookup,
                defaults=defaults,
            )
            action = "Created" if created else "Updated"
            style = self.style.SUCCESS if created else self.style.WARNING
            self.stdout.write(style(f"{action} category: {obj}"))
