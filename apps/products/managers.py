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
from django.db.models.functions import RowNumber

from apps.core.managers import ActiveQuerySet


class CategoryQuerySet(ActiveQuerySet):
    def with_products(self):
        Product = apps.get_model("products", "Product")
        queryset = Product.objects.order_by("name")
        return self.prefetch_related(
            Prefetch(
                "products",
                queryset=queryset,
                to_attr="all_products",
            ),
        )

    def with_active_products(self):
        Product = apps.get_model("products", "Product")
        queryset = Product.objects.active().order_by("name")
        return self.prefetch_related(
            Prefetch(
                "products",
                queryset=queryset,
                to_attr="active_products",
            ),
        )

    def with_products_count(self):
        return self.annotate(
            products_count=Count(
                "products",
                distinct=True,
            ),
        )

    def with_active_products_count(self):
        return self.annotate(
            active_products_count=Count(
                "products",
                filter=Q(products__is_active=True),
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
        return self.select_related("category")

    def with_variants(self):
        ProductVariant = apps.get_model("products", "ProductVariant")
        queryset = ProductVariant.objects.order_by("sort_order", "sku")
        return self.prefetch_related(
            Prefetch(
                "variants",
                queryset=queryset,
                to_attr="all_variants",
            ),
        )

    def with_active_variants(self):
        ProductVariant = apps.get_model("products", "ProductVariant")
        queryset = ProductVariant.objects.active().order_by("sort_order", "sku")
        return self.prefetch_related(
            Prefetch(
                "variants",
                queryset=queryset,
                to_attr="active_variants",
            ),
        )

    def with_images(self):
        ProductImage = apps.get_model("products", "ProductImage")
        queryset = ProductImage.objects.order_by("sort_order")
        return self.prefetch_related(
            Prefetch(
                "images",
                queryset=queryset,
                to_attr="all_images",
            ),
        )

    def with_active_images(self, limit=None):
        ProductImage = apps.get_model("products", "ProductImage")
        queryset = ProductImage.objects.active()
        if limit is not None:
            queryset = queryset.annotate(
                rn=Window(
                    expression=RowNumber(),
                    partition_by=[F("product_id")],
                    order_by=[F("sort_order").asc(), F("pk").asc()],
                ),
            ).filter(rn__lte=limit)
        queryset = queryset.order_by("sort_order", "pk")
        return self.prefetch_related(
            Prefetch(
                "images",
                queryset=queryset,
                to_attr="active_images",
            ),
        )

    def with_price_range(self):
        return self.annotate(
            min_price=Min(
                "variants__price",
                filter=Q(variants__is_active=True),
            ),
            max_price=Max(
                "variants__price",
                filter=Q(variants__is_active=True),
            ),
        )

    def with_total_stock_quantity(self):
        return self.annotate(
            total_stock_quantity=Sum(
                "variants__stock_quantity",
                filter=Q(variants__is_active=True),
            ),
        )


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    pass


class ProductVariantQuerySet(ActiveQuerySet):
    def with_product(self):
        return self.select_related("product")


class ProductVariantManager(models.Manager.from_queryset(ProductVariantQuerySet)):
    pass


class ProductImageQuerySet(ActiveQuerySet):
    def with_product(self):
        return self.select_related("product")


class ProductImageManager(models.Manager.from_queryset(ProductImageQuerySet)):
    pass
