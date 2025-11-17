from django.apps import apps
from django.db import models
from django.db.models import Count
from django.db.models import Prefetch
from django.db.models import Q


class BaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class BaseManager(models.Manager.from_queryset(BaseQuerySet)):
    pass


class CategoryQuerySet(BaseQuerySet):
    def _product_qs(self):
        return apps.get_model("products", "Product").objects

    def with_active_products(self):
        return self.prefetch_related(
            Prefetch(
                "products",
                queryset=self._product_qs().active().order_by("name"),
            ),
        )

    def with_active_products_count(self):
        return self.annotate(
            products_count=Count(
                "products",
                filter=Q(products__is_active=True),
                distinct=True,
            ),
        )

    def having_active_products(self):
        return self.filter(products__is_active=True).distinct()


class CategoryManager(BaseManager.from_queryset(CategoryQuerySet)):
    pass


class AttributeQuerySet(BaseQuerySet):
    def _attribute_value_qs(self):
        return apps.get_model("products", "AttributeValue").objects

    def with_values(self):
        return self.prefetch_related(
            Prefetch(
                "values",
                queryset=self._attribute_value_qs().order_by("sort_order"),
            ),
        )

    def with_active_values(self):
        return self.prefetch_related(
            Prefetch(
                "values",
                queryset=self._attribute_value_qs().active().order_by("sort_order"),
            ),
        )


class AttributeManager(BaseManager.from_queryset(AttributeQuerySet)):
    pass


class AttributeValueQuerySet(BaseQuerySet):
    def with_attribute(self):
        return self.select_related("attribute")


class AttributeValueManager(BaseManager.from_queryset(AttributeValueQuerySet)):
    def get_queryset(self):
        return super().get_queryset().with_attribute()


class ProductQuerySet(BaseQuerySet):
    def _product_variant_qs(self):
        return apps.get_model("products", "ProductVariant").objects

    def _product_variant_image_qs(self):
        return apps.get_model("products", "ProductVariantImage").objects

    def with_category(self):
        return self.select_related("category")

    def with_active_variants(self):
        return self.prefetch_related(
            Prefetch(
                "variants",
                queryset=self._product_variant_qs()
                .active()
                .order_by("sort_order", "sku")
                .prefetch_related(
                    Prefetch(
                        "images",
                        queryset=self._product_variant_image_qs()
                        .active()
                        .order_by("sort_order"),
                    ),
                ),
            ),
        )

    def with_price_range(self):
        return self.annotate(
            min_price=models.Min(
                "variants__price",
                filter=Q(variants__is_active=True),
            ),
            max_price=models.Max(
                "variants__price",
                filter=Q(variants__is_active=True),
            ),
        )


class ProductManager(BaseManager.from_queryset(ProductQuerySet)):
    pass


class ProductVariantQuerySet(BaseQuerySet):
    pass


class ProductVariantManager(BaseManager.from_queryset(ProductVariantQuerySet)):
    pass


class ProductVariantImageQuerySet(BaseQuerySet):
    def with_product_and_variant(self):
        return self.select_related("product_variant", "product_variant__product")


class ProductVariantImageManager(
    BaseManager.from_queryset(ProductVariantImageQuerySet),
):
    def get_queryset(self):
        return super().get_queryset().with_product_and_variant()
