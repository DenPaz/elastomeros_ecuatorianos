import pytest
from django.db import IntegrityError

from apps.core.utils import get_default_image_url

from .factories import CategoryFactory
from .factories import ProductFactory
from .factories import ProductVariantFactory
from .factories import ProductVariantImageFactory


@pytest.mark.django_db
class TestCategory:
    def test_str_method_returns_name(self):
        category = CategoryFactory(name="Electronics")
        assert str(category) == "Electronics"

    def test_unique_name_case_insensitive_constraint(self):
        CategoryFactory(name="Books", slug="books")
        with pytest.raises(IntegrityError):
            CategoryFactory(name="books", slug="books-1")

    def test_slug_field_is_unique(self):
        CategoryFactory(slug="toys")
        with pytest.raises(IntegrityError):
            CategoryFactory(slug="toys")

    def test_get_image_url_method_returns_default_when_no_image(self):
        category = CategoryFactory(image="")
        assert category.get_image_url() == get_default_image_url()

    def test_factory_post_generation_products(self):
        category = CategoryFactory(products=3)
        assert category.products.count() == 3  # noqa: PLR2004


@pytest.mark.django_db
class TestProduct:
    def test_str_method_returns_name(self):
        product = ProductFactory(name="Smartphone")
        assert str(product) == "Smartphone"

    def test_unique_name_per_category_case_insensitive_constraint(self):
        category = CategoryFactory()
        ProductFactory(category=category, name="Laptop", slug="laptop")
        with pytest.raises(IntegrityError):
            ProductFactory(category=category, name="laptop", slug="laptop-1")

    def test_same_name_allowed_in_different_categories(self):
        category1 = CategoryFactory()
        category2 = CategoryFactory()
        product1 = ProductFactory(category=category1, name="Desk", slug="desk")
        product2 = ProductFactory(category=category2, name="Desk", slug="desk-1")
        assert product1.name == product2.name
        assert product1.category != product2.category

    def test_slug_field_is_unique(self):
        ProductFactory(slug="headphones")
        with pytest.raises(IntegrityError):
            ProductFactory(slug="headphones")

    def test_factory_post_generation_variants(self):
        product = ProductFactory(variants=2)
        assert product.variants.count() == 2  # noqa: PLR2004


@pytest.mark.django_db
class TestProductVariant:
    def test_str_method_returns_product_name_and_sku(self):
        product = ProductFactory(name="Camera")
        variant = ProductVariantFactory(product=product, sku="CAM123")
        assert str(variant) == "Camera (SKU: CAM123)"

    def test_unique_variant_attributes_per_product_constraint(self):
        product = ProductFactory()
        ProductVariantFactory(
            product=product,
            attributes={"color": "red", "size": "M"},
        )
        with pytest.raises(IntegrityError):
            ProductVariantFactory(
                product=product,
                attributes={"color": "red", "size": "M"},
            )

    def test_same_attributes_allowed_in_different_products(self):
        product1 = ProductFactory()
        product2 = ProductFactory()
        variant1 = ProductVariantFactory(
            product=product1,
            attributes={"material": "cotton"},
        )
        variant2 = ProductVariantFactory(
            product=product2,
            attributes={"material": "cotton"},
        )
        assert variant1.attributes == variant2.attributes
        assert variant1.product != variant2.product

    def test_factory_post_generation_images(self):
        variant = ProductVariantFactory(images=2)
        assert variant.images.count() == 2  # noqa: PLR2004


@pytest.mark.django_db
class TestProductVariantImage:
    def test_str_method_returns_product_sku(self):
        variant = ProductVariantFactory(sku="VAR456")
        image = ProductVariantImageFactory(variant=variant)
        assert str(image) == f"Image for VAR456 (ID: {image.id})"
