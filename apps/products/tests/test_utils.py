# ruff: noqa: PLR2004
from unittest.mock import Mock

import pytest
from django.core.cache import cache

from apps.products.constants import ATTRIBUTES_SCHEMA_CACHE_KEY
from apps.products.constants import NO_ATTRIBUTES_SCHEMA
from apps.products.utils import build_attributes_schema
from apps.products.utils import get_attributes_schema
from apps.products.utils import get_default_attributes_schema
from apps.products.utils import get_product_image_upload_path

from .factories import AttributesSchemaFactory

pytestmark = pytest.mark.django_db


class TestGetDefaultAttributesSchema:
    def test_returns_dict_with_type_none(self):
        result = get_default_attributes_schema()
        assert result == {"type": "none"}


class TestBuildAttributesSchema:
    def test_returns_only_no_attributes_schema_when_no_schemas_exist(self):
        result = build_attributes_schema()
        assert result == {"type": "object", "oneOf": [NO_ATTRIBUTES_SCHEMA]}

    def test_includes_all_schemas_in_one_of(self):
        schema_1 = AttributesSchemaFactory()
        schema_2 = AttributesSchemaFactory()
        result = build_attributes_schema()
        assert result["type"] == "object"
        assert len(result["oneOf"]) == 3
        assert result["oneOf"][0] == NO_ATTRIBUTES_SCHEMA
        assert schema_1.schema in result["oneOf"]
        assert schema_2.schema in result["oneOf"]

    def test_no_attributes_schema_is_always_first(self):
        AttributesSchemaFactory()
        result = build_attributes_schema()
        assert result["oneOf"][0] is NO_ATTRIBUTES_SCHEMA


class TestGetAttributesSchema:
    def setup_method(self):
        cache.clear()

    def test_returns_built_schema_when_cache_is_empty(self):
        schema = AttributesSchemaFactory()
        result = get_attributes_schema()
        assert result["type"] == "object"
        assert schema.schema in result["oneOf"]

    def test_returns_cached_value_on_subsequent_calls(self):
        AttributesSchemaFactory()
        cache.set(ATTRIBUTES_SCHEMA_CACHE_KEY, {"cached": True})
        second = get_attributes_schema()
        assert second == {"cached": True}

    def test_accepts_instance_argument(self):
        result = get_attributes_schema(instance=Mock())
        assert result["type"] == "object"

    def test_rebuilds_after_cache_is_cleared(self):
        first_schema = AttributesSchemaFactory()
        first_result = get_attributes_schema()
        assert len(first_result["oneOf"]) == 2

        cache.delete(ATTRIBUTES_SCHEMA_CACHE_KEY)
        second_schema = AttributesSchemaFactory()
        second_result = get_attributes_schema()
        assert len(second_result["oneOf"]) == 3
        assert first_schema.schema in second_result["oneOf"]
        assert second_schema.schema in second_result["oneOf"]


class TestGetProductImageUploadPath:
    def test_returns_expected_path(self):
        instance = Mock()
        instance.product.slug = "industrial-o-ring"
        result = get_product_image_upload_path(instance, "photo.jpg")
        assert result == "products/products/industrial-o-ring/photo.jpg"

    def test_preserves_original_filename(self):
        instance = Mock()
        instance.product.slug = "gasket"
        result = get_product_image_upload_path(instance, "my image (1).png")
        assert result == "products/products/gasket/my image (1).png"
