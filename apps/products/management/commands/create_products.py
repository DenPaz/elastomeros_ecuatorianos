from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from slugify import slugify

from apps.products.models import Attribute
from apps.products.models import AttributeValue
from apps.products.models import Category
from apps.products.models import Product
from apps.products.models import ProductVariant
from apps.products.models import ProductVariantAttributeValue

data = [
    {
        "category_name": "Latex",
        "name": "Latex cremado",
        "slug": "latex-cremado",
        "short_description": (
            "Latex natural en estado cremoso, ideal para la "
            "fabricación de guantes y otros productos de caucho."
        ),
        "full_description": (
            "El latex cremado es un material versátil y de alta "
            "calidad, obtenido del látex natural del árbol de "
            "caucho. Su consistencia cremosa facilita su "
            "manipulación y procesamiento en la fabricación de "
            "diversos productos de caucho, como guantes, "
            "condones y artículos médicos. Este tipo de látex "
            "ofrece excelentes propiedades elásticas y de "
            "resistencia, asegurando la durabilidad y "
            "confort en los productos finales."
        ),
        "is_active": True,
        "variants": [
            {
                "sku": "LTX-CREM-1GAL",
                "price": "25.00",
                "stock": 35,
                "attributes": {
                    "Volumen del recipiente": "1 Galón",
                },
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "LTX-CREM-5GAL",
                "price": "110.00",
                "stock": 20,
                "attributes": {
                    "Volumen del recipiente": "5 Galones",
                },
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Productos de caucho",
        "name": "Guantes de caucho natural domésticos",
        "slug": "guantes-de-caucho-natural-domesticos",
        "short_description": (
            "Guantes de caucho natural diseñados para uso "
            "doméstico, ideales para tareas de limpieza y "
            "protección de las manos."
        ),
        "full_description": (
            "Nuestros guantes de caucho natural domésticos son "
            "la elección perfecta para proteger tus manos durante "
            "las tareas del hogar. Fabricados con caucho natural "
            "de alta calidad, estos guantes ofrecen una excelente "
            "elasticidad y resistencia, asegurando comodidad y "
            "durabilidad. Son ideales para lavar platos, limpiar "
            "superficies y manejar productos químicos domésticos, "
            "proporcionando una barrera efectiva contra la suciedad "
            "y los agentes irritantes. Disponibles en varios tamaños "
            "y colores, nuestros guantes se adaptan a tus necesidades "
            "diarias de limpieza."
        ),
        "is_active": True,
        "variants": [
            {
                "sku": "GUANT-DOM-AMAR-7",
                "price": "1.00",
                "stock": 100,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "7",
                },
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "GUANT-DOM-AMAR-75",
                "price": "1.00",
                "stock": 70,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "7.5",
                },
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "GUANT-DOM-AMAR-8",
                "price": "1.00",
                "stock": 80,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "8",
                },
                "sort_order": 2,
                "is_active": True,
            },
            {
                "sku": "GUANT-DOM-AMAR-85",
                "price": "1.00",
                "stock": 60,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "8.5",
                },
                "sort_order": 3,
                "is_active": True,
            },
            {
                "sku": "GUANT-DOM-AMAR-9",
                "price": "1.00",
                "stock": 90,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "9",
                },
                "sort_order": 4,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Productos de caucho",
        "name": "Guantes de caucho natural semi-industriales",
        "slug": "guantes-de-caucho-natural-semi-industriales",
        "short_description": (
            "Guantes de caucho natural diseñados para uso "
            "semi-industrial, ideales para tareas que requieren "
            "mayor resistencia y protección."
        ),
        "full_description": (
            "Nuestros guantes de caucho natural semi-industriales "
            "están diseñados para ofrecer una protección superior "
            "en entornos de trabajo que demandan mayor resistencia. "
            "Fabricados con caucho natural de alta calidad, estos "
            "guantes proporcionan una excelente elasticidad y durabilidad, "
            "asegurando comodidad durante largas jornadas laborales. "
            "Son ideales para tareas de manipulación de materiales, "
            "trabajos de construcción y otras actividades semi-industriales "
            "donde se requiere una barrera efectiva contra abrasiones, "
            "cortes y productos químicos. Disponibles en varios tamaños "
            "y colores, nuestros guantes se adaptan a las necesidades "
            "específicas de tu entorno de trabajo."
        ),
        "is_active": True,
        "variants": [
            {
                "sku": "GUANT-SEMI-AMAR-7",
                "price": "1.30",
                "stock": 50,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "7",
                },
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "GUANT-SEMI-AMAR-75",
                "price": "1.30",
                "stock": 40,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "7.5",
                },
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "GUANT-SEMI-AMAR-8",
                "price": "1.30",
                "stock": 60,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "8",
                },
                "sort_order": 2,
                "is_active": True,
            },
            {
                "sku": "GUANT-SEMI-AMAR-85",
                "price": "1.30",
                "stock": 30,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "8.5",
                },
                "sort_order": 3,
                "is_active": True,
            },
            {
                "sku": "GUANT-SEMI-AMAR-9",
                "price": "1.30",
                "stock": 70,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "9",
                },
                "sort_order": 4,
                "is_active": True,
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Create or update products and their variants in the database."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for entry in data:
            category_name = entry.pop("category_name")
            variants_data = entry.pop("variants", [])

            # 1. Get or create Category
            category_obj, category_created = Category.objects.get_or_create(
                name=category_name,
                defaults={"slug": slugify(category_name)},
            )
            if category_created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created category: {category_obj}"),
                )

            # 2. Create or update Product
            product_lookup = {"name": entry["name"], "category": category_obj}
            product_defaults = {
                k: v for k, v in entry.items() if k not in product_lookup
            }
            product_obj, product_created = Product.objects.update_or_create(
                **product_lookup,
                defaults=product_defaults,
            )
            if product_created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created product: {product_obj}"),
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Updated product: {product_obj}"),
                )

            for variant_entry in variants_data:
                attributes_data = variant_entry.pop("attributes", {})

                # 3. Create or update ProductVariant
                variant_lookup = {"sku": variant_entry["sku"]}
                variant_defaults = {
                    k: v for k, v in variant_entry.items() if k not in variant_lookup
                }
                variant_defaults["price"] = Decimal(variant_defaults["price"])
                variant_defaults["product"] = product_obj
                variant_obj, variant_created = ProductVariant.objects.update_or_create(
                    **variant_lookup,
                    defaults=variant_defaults,
                )
                if variant_created:
                    self.stdout.write(
                        self.style.SUCCESS(f"  - Created variant: {variant_obj}"),
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"  - Updated variant: {variant_obj}"),
                    )

                for attr_name, attr_value in attributes_data.items():
                    # 4. Get or create Attribute
                    attribute_obj, attribute_created = Attribute.objects.get_or_create(
                        name=attr_name,
                    )
                    if attribute_created:
                        self.stdout.write(
                            self.style.SUCCESS(f"    + Created attribute: {attr_name}"),
                        )

                    # 5. Get or create AttributeValue
                    attribute_value_obj, attribute_value_created = (
                        AttributeValue.objects.get_or_create(
                            attribute=attribute_obj,
                            value=attr_value,
                        )
                    )
                    if attribute_value_created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                (
                                    f"    + Created attribute value: {attr_value} "
                                    f"for attribute: {attr_name}",
                                ),
                            ),
                        )

                    # 6. Link AttributeValue to ProductVariant
                    _, pv_attr_created = (
                        ProductVariantAttributeValue.objects.update_or_create(
                            product_variant=variant_obj,
                            attribute_value=attribute_value_obj,
                        )
                    )
                    if pv_attr_created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                (
                                    f"    + Linked {attr_name}: {attr_value} "
                                    f"to variant {variant_obj.sku}"
                                ),
                            ),
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                (
                                    f"    ~ Updated link of {attr_name}: {attr_value} "
                                    f"to variant {variant_obj.sku}"
                                ),
                            ),
                        )
