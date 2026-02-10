from django.apps import apps
from django.core.cache import cache

from .constants import ATTRIBUTES_SCHEMA_CACHE_KEY
from .constants import NO_ATTRIBUTES_SCHEMA


def get_default_attributes_schema():
    return {"type": "none"}


def build_attributes_schema():
    AttributesSchema = apps.get_model("products", "AttributesSchema")
    schemas = list(AttributesSchema.objects.values_list("schema", flat=True))
    return {"type": "object", "oneOf": [NO_ATTRIBUTES_SCHEMA, *schemas]}


def get_attributes_schema(instance=None):
    return cache.get_or_set(
        ATTRIBUTES_SCHEMA_CACHE_KEY,
        build_attributes_schema,
        timeout=None,
    )


def get_product_image_upload_path(instance, filename):
    return f"products/products/{instance.product.slug}/{filename}"
