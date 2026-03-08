import pytest
from django.db import IntegrityError

from apps.core.utils import get_default_image_url

from .factories import AttributesSchemaFactory
from .factories import CategoryFactory
from .factories import ProductFactory
from .factories import ProductImageFactory
from .factories import ProductVariantFactory

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_slug_field_is_unique(self):
        CategoryFactory(slug="home-appliances")
        with pytest.raises(IntegrityError):
            CategoryFactory(slug="home-appliances")

    def test_unique_category_name_case_insensitive_constraint(self):
        CategoryFactory(name="Furniture")
        with pytest.raises(IntegrityError):
            CategoryFactory(name="furniture")

    def test_str_method_returns_name(self):
        category = CategoryFactory(name="Electronics")
        assert str(category) == "Electronics"

    @pytest.mark.skip(reason="URL pattern not implemented yet")
    def test_get_absolute_url_method(self):
        category = CategoryFactory(name="Books")
        url = category.get_absolute_url()
        assert url == "/products/?category=Books"

    def test_get_image_url_method_returns_default_when_no_image(self):
        category = CategoryFactory()
        assert category.get_image_url() == get_default_image_url()

    def test_product_count_property_returns_zero_when_not_annotated(self):
        category = CategoryFactory()
        assert category.product_count == 0


class TestAttributesSchemaModel:
    def test_unique_attributes_schema_name_case_insensitive_constraint(self):
        AttributesSchemaFactory(name="Size and Color")
        with pytest.raises(IntegrityError):
            AttributesSchemaFactory(name="size and color")

    def test_str_method_returns_name(self):
        schema = AttributesSchemaFactory(name="Material and Brand")
        assert str(schema) == "Material and Brand"

    def test_attributes_property_extracts_titles_from_schema(self):
        schema = AttributesSchemaFactory(
            schema={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "const": "test"},
                    "color": {"type": "string", "title": "Color"},
                    "size": {"type": "string", "title": "Size"},
                },
            },
        )
        assert schema.attributes == ["Color", "Size"]

    def test_attributes_property_uses_keys_as_fallback_when_no_title(self):
        schema = AttributesSchemaFactory(
            schema={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "const": "test"},
                    "material": {"type": "string"},
                },
            },
        )
        assert schema.attributes == ["material"]

    def test_attributes_property_ignores_type_field(self):
        schema = AttributesSchemaFactory(
            schema={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "const": "test"},
                },
            },
        )
        assert schema.attributes == []

    def test_attributes_property_returns_empty_list_for_empty_schema(self):
        schema = AttributesSchemaFactory(schema={})
        assert schema.attributes == []


class TestProductModel:
    def test_slug_field_is_unique(self):
        ProductFactory(slug="unique-product")
        with pytest.raises(IntegrityError):
            ProductFactory(slug="unique-product")

    def test_unique_product_name_per_category_case_insensitive_constraint(self):
        category = CategoryFactory(name="Toys")
        ProductFactory(name="Action Figure", category=category)
        with pytest.raises(IntegrityError):
            ProductFactory(name="action figure", category=category)

    def test_same_product_name_different_categories_allowed(self):
        category1 = CategoryFactory(name="Clothing")
        category2 = CategoryFactory(name="Accessories")
        product1 = ProductFactory(name="T-Shirt", slug="t-shirt", category=category1)
        product2 = ProductFactory(name="T-Shirt", slug="t-shirt-2", category=category2)
        assert product1.name == product2.name
        assert product1.category != product2.category

    def test_str_method_returns_name(self):
        product = ProductFactory(name="Smartphone")
        assert str(product) == "Smartphone"

    @pytest.mark.skip(reason="URL pattern not implemented yet")
    def test_get_absolute_url_method(self):
        product = ProductFactory(name="Laptop")
        url = product.get_absolute_url()
        assert url == "/products/laptop/"

    def test_price_range_property_returns_empty_string_when_not_annotated(self):
        product = ProductFactory()
        assert product.price_range == ""

    def test_total_stock_property_returns_zero_when_not_annotated(self):
        product = ProductFactory()
        assert product.total_stock == 0


class TestProductVariantModel:
    def test_sku_field_is_unique(self):
        ProductVariantFactory(sku="UNIQUE-SKU")
        with pytest.raises(IntegrityError):
            ProductVariantFactory(sku="UNIQUE-SKU")

    def test_unique_attributes_per_product_variant_constraint(self):
        product = ProductFactory(name="Shoes")
        schema = AttributesSchemaFactory(
            name="Shoe Attributes",
            schema={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "const": "shoe"},
                    "color": {"type": "string", "title": "Color"},
                    "size": {"type": "string", "title": "Size"},
                },
            },
        )
        ProductVariantFactory(
            product=product,
            sku="SHOE-001",
            attributes={"color": "Red", "size": "M"},
            attributes_schema=schema,
        )
        with pytest.raises(IntegrityError):
            ProductVariantFactory(
                product=product,
                sku="SHOE-002",
                attributes={"color": "Red", "size": "M"},
                attributes_schema=schema,
            )

    def test_str_method_returns_product_name_and_sku(self):
        product = ProductFactory(name="Headphones")
        variant = ProductVariantFactory(product=product, sku="HP-001")
        assert str(variant) == "Headphones (SKU: HP-001)"


class TestProductImageModel:
    def test_str_method_returns_product_name_and_image_id(self):
        product = ProductFactory(name="Camera")
        image = ProductImageFactory(product=product)
        assert str(image) == f"Image for Camera (ID: {image.id})"
