# ruff: noqa: PLR2004
from decimal import Decimal

import pytest

from apps.products.models import Category
from apps.products.models import Product
from apps.products.models import ProductImage
from apps.products.models import ProductVariant

from .factories import CategoryFactory
from .factories import ProductFactory
from .factories import ProductImageFactory
from .factories import ProductVariantFactory

pytestmark = pytest.mark.django_db


class TestCategoryQuerySet:
    def test_active_method_returns_only_active_categories(self):
        active_category = CategoryFactory(is_active=True)
        inactive_category = CategoryFactory(is_active=False)
        queryset = Category.objects.active()
        assert active_category in queryset
        assert inactive_category not in queryset

    def test_with_products_method_prefetches_active_products(self):
        category = CategoryFactory(
            products=[
                {"is_active": True},
                {"is_active": True},
                {"is_active": False},
            ],
        )
        queryset = Category.objects.with_products(active_only=True)
        category_from_queryset = queryset.get(id=category.id)
        assert hasattr(category_from_queryset, "active_products")
        assert len(category_from_queryset.active_products) == 2
        for product in category_from_queryset.active_products:
            assert product.is_active

    def test_with_products_method_prefetches_all_products(self):
        category = CategoryFactory(
            products=[
                {"is_active": True},
                {"is_active": True},
                {"is_active": False},
            ],
        )
        queryset = Category.objects.with_products(active_only=False)
        category_from_queryset = queryset.get(id=category.id)
        assert hasattr(category_from_queryset, "all_products")
        assert len(category_from_queryset.all_products) == 3
        for product in category_from_queryset.all_products:
            assert product in category.products.all()

    def test_with_products_method_orders_products_by_name(self):
        category = CategoryFactory(
            products=[
                {"name": "Banana"},
                {"name": "Apple"},
                {"name": "Cherry"},
            ],
        )
        queryset = Category.objects.with_products(active_only=False)
        category_from_queryset = queryset.get(id=category.id)
        assert hasattr(category_from_queryset, "all_products")
        assert len(category_from_queryset.all_products) == 3
        expected_order = ["Apple", "Banana", "Cherry"]
        actual_order = [product.name for product in category_from_queryset.all_products]
        assert actual_order == expected_order

    def test_with_product_count_method_counts_active_products(self):
        category = CategoryFactory(
            products=[
                {"is_active": True},
                {"is_active": True},
                {"is_active": False},
            ],
        )
        queryset = Category.objects.with_product_count(active_only=True)
        category_from_queryset = queryset.get(id=category.id)
        assert hasattr(category_from_queryset, "_product_count")
        assert category_from_queryset._product_count == 2  # noqa: SLF001

    def test_with_product_count_method_counts_all_products(self):
        category = CategoryFactory(
            products=[
                {"is_active": True},
                {"is_active": True},
                {"is_active": False},
            ],
        )
        queryset = Category.objects.with_product_count(active_only=False)
        category_from_queryset = queryset.get(id=category.id)
        assert hasattr(category_from_queryset, "_product_count")
        assert category_from_queryset._product_count == 3  # noqa: SLF001


class TestProductQuerySet:
    def test_active_method_returns_only_active_products(self):
        active_product = ProductFactory(is_active=True)
        inactive_product = ProductFactory(is_active=False)
        queryset = Product.objects.active()
        assert active_product in queryset
        assert inactive_product not in queryset

    def test_with_category_method_avoids_extra_queries(self, django_assert_num_queries):
        category = CategoryFactory()
        product = ProductFactory(category=category)
        with django_assert_num_queries(1):
            queryset = Product.objects.with_category()
            product_from_queryset = queryset.get(id=product.id)
            assert product_from_queryset.category == category

    def test_with_variants_method_prefetches_active_variants(self):
        product = ProductFactory(
            variants=[
                {"is_active": True},
                {"is_active": True},
                {"is_active": False},
            ],
        )
        queryset = Product.objects.with_variants(active_only=True)
        product_from_queryset = queryset.get(id=product.id)
        assert hasattr(product_from_queryset, "active_variants")
        assert len(product_from_queryset.active_variants) == 2
        for variant in product_from_queryset.active_variants:
            assert variant.is_active

    def test_with_variants_method_prefetches_all_variants(self):
        product = ProductFactory(
            variants=[
                {"is_active": True},
                {"is_active": True},
                {"is_active": False},
            ],
        )
        queryset = Product.objects.with_variants(active_only=False)
        product_from_queryset = queryset.get(id=product.id)
        assert hasattr(product_from_queryset, "all_variants")
        assert len(product_from_queryset.all_variants) == 3
        for variant in product_from_queryset.all_variants:
            assert variant in product.variants.all()

    def test_with_variants_method_orders_variants_by_sort_order_and_sku(self):
        product = ProductFactory(
            variants=[
                {"sort_order": 2, "sku": "B"},
                {"sort_order": 1, "sku": "C"},
                {"sort_order": 1, "sku": "A"},
            ],
        )
        queryset = Product.objects.with_variants(active_only=False)
        product_from_queryset = queryset.get(id=product.id)
        assert hasattr(product_from_queryset, "all_variants")
        assert len(product_from_queryset.all_variants) == 3
        expected_order = ["A", "C", "B"]
        actual_order = [variant.sku for variant in product_from_queryset.all_variants]
        assert actual_order == expected_order

    def test_with_variants_method_avoids_extra_queries(self, django_assert_num_queries):
        product = ProductFactory(variants=10)
        with django_assert_num_queries(2):
            queryset = Product.objects.with_variants(active_only=False)
            product_from_queryset = queryset.get(id=product.id)
            assert len(product_from_queryset.all_variants) == 10

    def test_with_images_method_prefetches_active_images(self):
        product = ProductFactory(
            images=[
                {"is_active": True},
                {"is_active": True},
                {"is_active": False},
            ],
        )
        queryset = Product.objects.with_images(active_only=True)
        product_from_queryset = queryset.get(id=product.id)
        assert hasattr(product_from_queryset, "active_images")
        assert len(product_from_queryset.active_images) == 2
        for image in product_from_queryset.active_images:
            assert image.is_active

    def test_with_images_method_prefetches_all_images(self):
        product = ProductFactory(
            images=[
                {"is_active": True},
                {"is_active": True},
                {"is_active": False},
            ],
        )
        queryset = Product.objects.with_images(active_only=False)
        product_from_queryset = queryset.get(id=product.id)
        assert hasattr(product_from_queryset, "all_images")
        assert len(product_from_queryset.all_images) == 3
        for image in product_from_queryset.all_images:
            assert image in product.images.all()

    def test_with_images_method_prefetches_limited_images(self):
        product = ProductFactory(images=3)
        queryset = Product.objects.with_images(active_only=False, limit=2)
        product_from_queryset = queryset.get(id=product.id)
        assert len(product_from_queryset.all_images) == 2
        expected_images = list(product.images.all()[:2])
        assert product_from_queryset.all_images == expected_images

    def test_with_images_method_orders_images_by_sort_order_and_id(self):
        product = ProductFactory(
            images=[
                {"sort_order": 2},
                {"sort_order": 1},
                {"sort_order": 1},
            ],
        )
        queryset = Product.objects.with_images(active_only=False)
        product_from_queryset = queryset.get(id=product.id)
        assert hasattr(product_from_queryset, "all_images")
        assert len(product_from_queryset.all_images) == 3
        expected_order = sorted(
            product.images.all(),
            key=lambda img: (img.sort_order, img.id),
        )
        assert product_from_queryset.all_images == expected_order

    def test_with_price_range_method_calculates_price_range_for_active_variants(self):
        product = ProductFactory(
            variants=[
                {"price": Decimal("10.00"), "is_active": True},
                {"price": Decimal("20.00"), "is_active": True},
                {"price": Decimal("30.00"), "is_active": False},
            ],
        )
        queryset = Product.objects.with_price_range(active_only=True)
        product_from_queryset = queryset.get(id=product.id)
        assert hasattr(product_from_queryset, "_min_price")
        assert hasattr(product_from_queryset, "_max_price")
        assert product_from_queryset._min_price == Decimal("10.00")  # noqa: SLF001
        assert product_from_queryset._max_price == Decimal("20.00")  # noqa: SLF001

    def test_with_price_range_method_calculates_price_range_for_all_variants(self):
        product = ProductFactory(
            variants=[
                {"price": Decimal("10.00"), "is_active": True},
                {"price": Decimal("20.00"), "is_active": True},
                {"price": Decimal("30.00"), "is_active": False},
            ],
        )
        queryset = Product.objects.with_price_range(active_only=False)
        product_from_queryset = queryset.get(id=product.id)
        assert hasattr(product_from_queryset, "_min_price")
        assert hasattr(product_from_queryset, "_max_price")
        assert product_from_queryset._min_price == Decimal("10.00")  # noqa: SLF001
        assert product_from_queryset._max_price == Decimal("30.00")  # noqa: SLF001

    def test_with_total_stock_method_calculates_total_stock_for_active_variants(self):
        product = ProductFactory(
            variants=[
                {"stock": 10, "is_active": True},
                {"stock": 20, "is_active": True},
                {"stock": 30, "is_active": False},
            ],
        )
        queryset = Product.objects.with_total_stock(active_only=True)
        product_from_queryset = queryset.get(id=product.id)
        assert hasattr(product_from_queryset, "_total_stock")
        assert product_from_queryset._total_stock == 30  # noqa: SLF001

    def test_with_total_stock_method_calculates_total_stock_for_all_variants(self):
        product = ProductFactory(
            variants=[
                {"stock": 10, "is_active": True},
                {"stock": 20, "is_active": True},
                {"stock": 30, "is_active": False},
            ],
        )
        queryset = Product.objects.with_total_stock(active_only=False)
        product_from_queryset = queryset.get(id=product.id)
        assert hasattr(product_from_queryset, "_total_stock")
        assert product_from_queryset._total_stock == 60  # noqa: SLF001


class TestProductVariantQuerySet:
    def test_active_method_returns_only_active_variants(self):
        product = ProductFactory()
        active_variant = ProductVariantFactory(product=product, is_active=True)
        inactive_variant = ProductVariantFactory(product=product, is_active=False)
        queryset = ProductVariant.objects.active()
        assert active_variant in queryset
        assert inactive_variant not in queryset

    def test_with_product_method_avoids_extra_queries(self, django_assert_num_queries):
        product = ProductFactory()
        variant = ProductVariantFactory(product=product)
        with django_assert_num_queries(1):
            queryset = ProductVariant.objects.with_product()
            variant_from_queryset = queryset.get(id=variant.id)
            assert variant_from_queryset.product == product


class TestProductImageQuerySet:
    def test_active_method_returns_only_active_images(self):
        product = ProductFactory()
        active_image = ProductImageFactory(product=product, is_active=True)
        inactive_image = ProductImageFactory(product=product, is_active=False)
        queryset = ProductImage.objects.active()
        assert active_image in queryset
        assert inactive_image not in queryset

    def test_with_product_method_avoids_extra_queries(self, django_assert_num_queries):
        product = ProductFactory()
        image = ProductImageFactory(product=product)
        with django_assert_num_queries(1):
            queryset = ProductImage.objects.with_product()
            image_from_queryset = queryset.get(id=image.id)
            assert image_from_queryset.product == product
