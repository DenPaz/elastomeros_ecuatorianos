from django.apps import apps
from django.core.cache import cache

ATTR_SCHEMA_CACHE_KEY = "products:attributes_schema:oneof:v1"

NO_ATTRIBUTES_SCHEMA = {
    "type": "object",
    "title": "No attributes",
    "required": ["type"],
    "additionalProperties": False,
    "properties": {
        "type": {
            "type": "string",
            "const": "none",
            "widget": "hidden",
            "readonly": True,
        },
    },
}


def get_default_attributes_schema():
    return {"type": "none"}


def build_attributes_schema():
    AttributesSchema = apps.get_model("products", "AttributesSchema")
    schemas = list(AttributesSchema.objects.values_list("schema", flat=True))
    return {"type": "object", "oneOf": [NO_ATTRIBUTES_SCHEMA, *schemas]}


def get_attributes_schema(instance=None):
    return cache.get_or_set(
        ATTR_SCHEMA_CACHE_KEY,
        build_attributes_schema,
        timeout=None,
    )


def get_product_image_upload_path(instance, filename):
    return f"products/products/{instance.product.slug}/{filename}"
