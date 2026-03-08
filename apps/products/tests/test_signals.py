import pytest
from django.core.cache import cache

from apps.products.constants import ATTRIBUTES_SCHEMA_CACHE_KEY

from .factories import AttributesSchemaFactory

pytestmark = pytest.mark.django_db


class TestClearAttributesSchemaCacheSignal:
    def setup_method(self):
        cache.clear()

    def test_cache_cleared_on_schema_create(self):
        cache.set(ATTRIBUTES_SCHEMA_CACHE_KEY, "cached_value")
        AttributesSchemaFactory()
        assert cache.get(ATTRIBUTES_SCHEMA_CACHE_KEY) is None

    def test_cache_cleared_on_schema_update(self):
        schema = AttributesSchemaFactory()
        cache.set(ATTRIBUTES_SCHEMA_CACHE_KEY, "cached_value")
        schema.name = "Updated Name"
        schema.save()
        assert cache.get(ATTRIBUTES_SCHEMA_CACHE_KEY) is None

    def test_cache_cleared_on_schema_delete(self):
        schema = AttributesSchemaFactory()
        cache.set(ATTRIBUTES_SCHEMA_CACHE_KEY, "cached_value")
        schema.delete()
        assert cache.get(ATTRIBUTES_SCHEMA_CACHE_KEY) is None
