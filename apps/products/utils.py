from django.apps import apps
from django.core.cache import cache

from .constants import ATTRIBUTES_SCHEMA_CACHE_KEY
from .constants import NO_ATTRIBUTES_SCHEMA


def get_default_attributes_schema() -> dict:
    """Return the default attributes value for new product variants."""
    return {"type": "none"}


def build_attributes_schema() -> dict:
    """Build the full JSON Schema with all attribute schemas as oneOf options."""
    AttributesSchema = apps.get_model("products", "AttributesSchema")
    schemas = list(AttributesSchema.objects.values_list("schema", flat=True))
    return {"type": "object", "oneOf": [NO_ATTRIBUTES_SCHEMA, *schemas]}


def get_attributes_schema(instance=None):
    """Return the cached attributes schema, building it if not cached."""
    return cache.get_or_set(
        ATTRIBUTES_SCHEMA_CACHE_KEY,
        build_attributes_schema,
        timeout=None,
    )


def get_product_image_upload_path(instance, filename) -> str:
    """Return the upload path for a product image."""
    return f"products/products/{instance.product.slug}/{filename}"
