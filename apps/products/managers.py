from django.apps import apps
from django.db import models
from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from django.db.models import Prefetch
from django.db.models import Q


class BaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class BaseManager(models.Manager.from_queryset(BaseQuerySet)):
    pass


class CategoryQuerySet(BaseQuerySet):
    def _product_queryset(self):
        return apps.get_model("products", "Product").objects

    def with_products(self):
        queryset = self._product_queryset().active().order_by("name")
        return self.prefetch_related(
            Prefetch(
                "products",
                queryset=queryset,
                to_attr="active_products",
            ),
        )

    def with_products_count(self):
        queryset = self._product_queryset().active()
        return self.annotate(
            product_count=Count(
                "products",
                filter=Q(products__in=queryset),
                distinct=True,
            ),
        )


class CategoryManager(models.Manager.from_queryset(CategoryQuerySet)):
    pass


class AttributeQuerySet(BaseQuerySet):
    def _attribute_value_queryset(self):
        return apps.get_model("products", "AttributeValue").objects

    def with_attribute_values(self):
        queryset = (
            self._attribute_value_queryset()
            .active()
            .order_by(
                "sort_order",
                "value",
            )
        )
        return self.prefetch_related(
            Prefetch(
                "attribute_values",
                queryset=queryset,
                to_attr="active_attribute_values",
            ),
        )


class AttributeManager(models.Manager.from_queryset(AttributeQuerySet)):
    pass


class AttributeValueQuerySet(BaseQuerySet):
    def with_attribute(self):
        return self.select_related("attribute")


class AttributeValueManager(models.Manager.from_queryset(AttributeValueQuerySet)):
    def get_queryset(self):
        return super().get_queryset().with_attribute()


class ProductQuerySet(BaseQuerySet):
    def _product_variant_queryset(self):
        return apps.get_model("products", "ProductVariant").objects

    def _product_image_queryset(self):
        return apps.get_model("products", "ProductImage").objects

    def with_category(self):
        return self.select_related("category")

    def with_variants_and_images(self):
        variant_queryset = (
            self._product_variant_queryset()
            .active()
            .order_by(
                "sort_order",
                "sku",
            )
        )
        image_queryset = (
            self._product_image_queryset()
            .active()
            .order_by(
                "sort_order",
            )
        )
        return self.prefetch_related(
            Prefetch(
                "variants",
                queryset=variant_queryset,
            ),
            Prefetch(
                "images",
                queryset=image_queryset,
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


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    def get_queryset(self):
        return super().get_queryset().with_category()


class ProductVariantQuerySet(BaseQuerySet):
    def with_product(self):
        return self.select_related("product")

    def available(self):
        return self.active().filter(stock__gt=0)


class ProductVariantManager(models.Manager.from_queryset(ProductVariantQuerySet)):
    def get_queryset(self):
        return super().get_queryset().with_product()


class ProductVariantAttributeValueQuerySet(models.QuerySet):
    def with_related_fields(self):
        return self.select_related(
            "product_variant",
            "product_variant__product",
            "attribute_value",
            "attribute_value__attribute",
        )


class ProductVariantAttributeValueManager(
    models.Manager.from_queryset(ProductVariantAttributeValueQuerySet),
):
    pass


class ProductImageQuerySet(BaseQuerySet):
    def with_product_and_variant(self):
        return self.select_related("product", "product_variant")


class ProductImageManager(models.Manager.from_queryset(ProductImageQuerySet)):
    def get_queryset(self):
        return super().get_queryset().with_product_and_variant()
