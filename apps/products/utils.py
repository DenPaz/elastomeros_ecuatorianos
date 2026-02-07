from django.apps import apps


def get_default_attributes_schema():
    return {"type": "none"}


def get_attributes_schema():
    AttributesSchema = apps.get_model("products", "AttributesSchema")
    schemas = AttributesSchema.objects.values_list("schema", flat=True)
    return {
        "type": "object",
        "oneOf": [
            {
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
            },
            *schemas,
        ],
    }


def get_product_image_upload_path(instance, filename):
    return f"products/products/{instance.product.slug}/{filename}"
