import random

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.products.models import Category
from apps.products.models import Product
from apps.products.models import ProductVariant
from apps.products.models import ProductVariantImage
from apps.products.tests.factories import CategoryFactory
from apps.products.tests.factories import ProductFactory
from apps.products.tests.factories import ProductVariantFactory
from apps.products.tests.factories import ProductVariantImageFactory

COLORS = ["red", "green", "blue", "yellow", "purple", "orange", "black"]


class Command(BaseCommand):
    help = "Seed the database with sample products, categories, variants, and images."

    def add_arguments(self, parser):
        parser.add_argument("--categories", type=int, default=10)
        parser.add_argument("--products-per-category", type=int, default=25)
        parser.add_argument("--variants-per-product", type=int, default=5)
        parser.add_argument("--images-per-variant", type=int, default=4)
        parser.add_argument("--with-category-images", action="store_true")
        parser.add_argument("--clear", action="store_true")
        parser.add_argument("--seed", type=int, default=42)

    @transaction.atomic
    def handle(self, *args, **kwargs):
        rng = random.Random(kwargs["seed"])  # noqa: S311

        if kwargs["clear"]:
            ProductVariantImage.objects.all().delete()
            ProductVariant.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Cleared existing product data."))

        for _ in range(kwargs["categories"]):
            category = CategoryFactory(with_image=kwargs["with_category_images"])
            for _ in range(kwargs["products_per_category"]):
                product = ProductFactory(category=category)
                for _ in range(kwargs["variants_per_product"]):
                    variant = ProductVariantFactory(product=product)
                    for _ in range(kwargs["images_per_variant"]):
                        ProductVariantImageFactory(
                            variant=variant,
                            image__width=rng.randint(100, 200),
                            image__height=rng.randint(100, 200),
                            image__color=rng.choice(COLORS),
                        )
        self.stdout.write(self.style.SUCCESS("Successfully seeded product data."))
