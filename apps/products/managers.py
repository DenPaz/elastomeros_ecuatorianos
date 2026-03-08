from django.apps import apps
from django.db import models
from django.db.models import Count
from django.db.models import F
from django.db.models import Max
from django.db.models import Min
from django.db.models import Prefetch
from django.db.models import Q
from django.db.models import Sum
from django.db.models import Window
from django.db.models.functions import Coalesce
from django.db.models.functions import RowNumber

from apps.core.managers import ActiveQuerySet


class CategoryQuerySet(ActiveQuerySet):
    def with_products(self, *, active_only=True):
        """Prefetch related products, ordered by name."""
        Product = apps.get_model("products", "Product")
        queryset = Product.objects.active() if active_only else Product.objects.all()
        queryset = queryset.order_by("name")
        return self.prefetch_related(
            Prefetch(
                "products",
                queryset=queryset,
                to_attr="active_products" if active_only else "all_products",
            ),
        )

    def with_product_count(self, *, active_only=True):
        """Annotate each category with its product count."""
        product_filter = Q(products__is_active=True) if active_only else Q()
        return self.annotate(
            _product_count=Count(
                "products",
                filter=product_filter,
                distinct=True,
            ),
        )


class CategoryManager(models.Manager.from_queryset(CategoryQuerySet)):
    pass


class AttributesSchemaQuerySet(models.QuerySet):
    pass


class AttributesSchemaManager(models.Manager.from_queryset(AttributesSchemaQuerySet)):
    pass


class ProductQuerySet(ActiveQuerySet):
    def with_category(self):
        """Select related category in the same query."""
        return self.select_related("category")

    def with_variants(self, *, active_only=True):
        """Prefetch related variants, ordered by sort order and SKU."""
        ProductVariant = apps.get_model("products", "ProductVariant")
        queryset = (
            ProductVariant.objects.active()
            if active_only
            else ProductVariant.objects.all()
        )
        queryset = queryset.order_by("sort_order", "sku")
        return self.prefetch_related(
            Prefetch(
                "variants",
                queryset=queryset,
                to_attr="active_variants" if active_only else "all_variants",
            ),
        )

    def with_images(self, *, active_only=True, limit=None):
        """Prefetch related images, ordered by sort order and ID."""
        ProductImage = apps.get_model("products", "ProductImage")
        queryset = (
            ProductImage.objects.active() if active_only else ProductImage.objects.all()
        )
        if limit is not None:
            queryset = queryset.annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F("product_id")],
                    order_by=[F("sort_order").asc(), F("id").asc()],
                ),
            ).filter(row_number__lte=limit)
        queryset = queryset.order_by("sort_order", "id")
        return self.prefetch_related(
            Prefetch(
                "images",
                queryset=queryset,
                to_attr="active_images" if active_only else "all_images",
            ),
        )

    def with_price_range(self, *, active_only=True):
        """Annotate each product with its minimum and maximum variant price."""
        variant_filter = Q(variants__is_active=True) if active_only else Q()
        return self.annotate(
            min_price=Min(
                "variants__price",
                filter=variant_filter,
            ),
            max_price=Max(
                "variants__price",
                filter=variant_filter,
            ),
        )

    def with_total_stock(self, *, active_only=True):
        """Annotate each product with the sum of its variant stock."""
        variant_filter = Q(variants__is_active=True) if active_only else Q()
        return self.annotate(
            _total_stock=Coalesce(
                Sum("variants__stock", filter=variant_filter),
                0,
            ),
        )


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    pass


class ProductVariantQuerySet(ActiveQuerySet):
    def with_product(self):
        """Select related product in the same query."""
        return self.select_related("product")


class ProductVariantManager(models.Manager.from_queryset(ProductVariantQuerySet)):
    pass


class ProductImageQuerySet(ActiveQuerySet):
    def with_product(self):
        """Select related product in the same query."""
        return self.select_related("product")


class ProductImageManager(models.Manager.from_queryset(ProductImageQuerySet)):
    pass
