from django.utils.translation import gettext_lazy as _

NO_SPECIFICATION_SCHEMA = {
    "type": "object",
    "title": _("No specification"),
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

RUBBER_GLOVES_SCHEMA = {
    "type": "object",
    "title": _("Rubber gloves"),
    "required": ["type", "color", "size"],
    "additionalProperties": False,
    "properties": {
        "type": {
            "type": "string",
            "const": "rubber_gloves",
            "widget": "hidden",
            "readonly": True,
        },
        "color": {
            "type": "string",
            "title": _("Color"),
            "choices": [
                {
                    "title": _("Black"),
                    "value": "black",
                },
                {
                    "title": _("Yellow"),
                    "value": "yellow",
                },
                {
                    "title": _("Yellow/Black"),
                    "value": "yellow_black",
                },
            ],
        },
        "size": {
            "type": "number",
            "title": _("Size"),
            "choices": [7, 7.5, 8, 8.5, 9, 9.5, 10],
        },
    },
}

NATURAL_LATEX_SCHEMA = {
    "type": "object",
    "title": _("Natural latex"),
    "required": ["type", "volume_gal"],
    "additionalProperties": False,
    "properties": {
        "type": {
            "type": "string",
            "const": "natural_latex",
            "widget": "hidden",
            "readonly": True,
        },
        "volume_gal": {
            "type": "number",
            "title": _("Volume (gal)"),
            "minimum": 0,
        },
    },
}

PRODUCT_SPECIFICATION_SCHEMA = {
    "type": "object",
    "oneOf": [
        NO_SPECIFICATION_SCHEMA,
        RUBBER_GLOVES_SCHEMA,
        NATURAL_LATEX_SCHEMA,
    ],
}


def get_default_product_specification():
    return {"type": "none"}
