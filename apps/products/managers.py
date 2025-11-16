from django.apps import apps
from django.db import models
from django.db.models import Count
from django.db.models import Prefetch
from django.db.models import Q


class BaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class BaseManager(models.Manager.from_queryset(BaseQuerySet)):
    pass


class CategoryQuerySet(BaseQuerySet):
    def _product_model(self):
        return apps.get_model("products", "Product")

    def with_products(self):
        product = self._product_model()
        queryset = product.objects.all()
        return self.prefetch_related(Prefetch("products", queryset=queryset))

    def with_active_products(self):
        product = self._product_model()
        queryset = product.objects.filter(is_active=True)
        return self.prefetch_related(Prefetch("products", queryset=queryset))

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


class CategoryManager(BaseManager.from_queryset(CategoryQuerySet)):
    pass


class AttributeQuerySet(BaseQuerySet):
    def _attribute_value_model(self):
        return apps.get_model("products", "AttributeValue")

    def with_values(self):
        attribute_value = self._attribute_value_model()
        queryset = attribute_value.objects.all()
        return self.prefetch_related(Prefetch("values", queryset=queryset))

    def with_active_values(self):
        attribute_value = self._attribute_value_model()
        queryset = attribute_value.objects.filter(is_active=True)
        return self.prefetch_related(Prefetch("values", queryset=queryset))


class AttributeManager(BaseManager.from_queryset(AttributeQuerySet)):
    pass


class AttributeValueQuerySet(BaseQuerySet):
    def with_attribute(self):
        return self.select_related("attribute")

    def for_attribute(self, attribute):
        attr_id = getattr(attribute, "pk", attribute)
        return self.filter(attribute_id=attr_id)


class AttributeValueManager(BaseManager.from_queryset(AttributeValueQuerySet)):
    def get_queryset(self):
        return super().get_queryset().with_attribute()


class ProductQuerySet(BaseQuerySet):
    pass


class ProductManager(BaseManager.from_queryset(ProductQuerySet)):
    pass


class ProductVariantQuerySet(BaseQuerySet):
    pass


class ProductVariantManager(BaseManager.from_queryset(ProductVariantQuerySet)):
    pass


class ProductVariantImageQuerySet(BaseQuerySet):
    pass


class ProductVariantImageManager(
    BaseManager.from_queryset(ProductVariantImageQuerySet),
):
    pass


class ProductVariantAttributeValueQuerySet(BaseQuerySet):
    pass


class ProductVariantAttributeValueManager(
    BaseManager.from_queryset(ProductVariantAttributeValueQuerySet),
):
    pass
