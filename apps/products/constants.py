ATTRIBUTES_SCHEMA_CACHE_KEY = "products:attributes_schema:v1"
NO_ATTRIBUTES_SCHEMA = {
    "type": "object",
    "title": "No attributes",
    "required": ["type"],
    "properties": {
        "type": {
            "type": "string",
            "const": "none",
            "widget": "hidden",
            "readonly": True,
        },
    },
    "additionalProperties": False,
}
CATEGORIES_CACHE_KEY = "products:categories:v1"
