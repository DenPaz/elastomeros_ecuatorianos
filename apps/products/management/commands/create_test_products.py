from django.core.management.base import BaseCommand
from django.db import transaction

from apps.products.models import AttributesSchema
from apps.products.models import Category
from apps.products.models import Product
from apps.products.models import ProductImage
from apps.products.models import ProductVariant
from apps.products.tests.factories import CategoryFactory


class Command(BaseCommand):
    help = "Create test products for development and testing purposes."

    def add_arguments(self, parser):
        parser.add_argument("--categories", type=int, default=10)
        parser.add_argument("--with-category-images", action="store_true")
        parser.add_argument("--products-per-category", type=int, default=10)
        parser.add_argument("--variants-per-product", type=int, default=3)
        parser.add_argument("--images-per-product", type=int, default=3)
        parser.add_argument("--clean", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        categories = options["categories"]
        with_category_images = options["with_category_images"]
        products_per_category = options["products_per_category"]
        variants_per_product = options["variants_per_product"]
        images_per_product = options["images_per_product"]
        clean = options["clean"]

        if clean:
            ProductImage.objects.all().delete()
            ProductVariant.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            AttributesSchema.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Cleared existing product data."))

        for _ in range(categories):
            CategoryFactory(
                with_image=with_category_images,
                products=products_per_category,
                products__variants=variants_per_product,
                products__images=images_per_product,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {categories} categories with "
                f"{products_per_category} products each, "
                f"{variants_per_product} variants per product, and "
                f"{images_per_product} images per product.",
            ),
        )
