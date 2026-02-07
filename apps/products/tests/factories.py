from django.utils.text import slugify
from factory import Faker
from factory import LazyAttribute
from factory import Sequence
from factory import SubFactory
from factory import Trait
from factory import post_generation
from factory.django import DjangoModelFactory
from factory.django import ImageField

from apps.products.models import AttributesSchema
from apps.products.models import Category
from apps.products.models import Product
from apps.products.models import ProductImage
from apps.products.models import ProductVariant


class CategoryFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"Category {n + 1}")
    slug = LazyAttribute(lambda obj: slugify(obj.name))
    description = Faker("paragraph")
    is_active = True

    class Meta:
        model = Category
        skip_postgeneration_save = True

    class Params:
        with_image = Trait(
            image=ImageField(
                filename=Sequence(lambda n: f"category_image_{n + 1}.jpg"),
            ),
        )

    @post_generation
    def products(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        for _ in range(extracted):
            ProductFactory(category=self, **kwargs)


class ProductFactory(DjangoModelFactory):
    category = SubFactory(CategoryFactory)
    name = Sequence(lambda n: f"Product {n + 1}")
    slug = LazyAttribute(lambda obj: slugify(obj.name))
    short_description = Faker("sentence")
    full_description = Faker("paragraph")
    is_active = True

    class Meta:
        model = Product
        skip_postgeneration_save = True

    @post_generation
    def variants(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        for _ in range(extracted):
            ProductVariantFactory(product=self, **kwargs)

    @post_generation
    def images(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        for _ in range(extracted):
            ProductImageFactory(product=self, **kwargs)


def build_schema(index: int, n_attributes: int) -> dict:
    schema = {
        "type": "object",
        "title": f"Attributes Schema {index}",
        "required": ["type"],
        "additionalProperties": False,
        "properties": {
            "type": {
                "type": "string",
                "const": f"attributes_schema_{index}",
                "widget": "hidden",
                "readonly": True,
            },
        },
    }
    for i in range(1, n_attributes + 1):
        schema["properties"][f"attribute_{i}"] = {
            "type": "string",
            "title": f"Attribute {i}",
        }
    return schema


class AttributesSchemaFactory(DjangoModelFactory):
    schema_index = Sequence(lambda n: n + 1)
    n_attributes = Faker("pyint", min_value=1, max_value=4)

    name = Sequence(lambda n: f"Attributes schema {n + 1}")
    schema = LazyAttribute(lambda o: build_schema(o.schema_index, o.n_attributes))

    class Meta:
        model = AttributesSchema
        exclude = ("schema_index", "n_attributes")


class ProductVariantFactory(DjangoModelFactory):
    product = SubFactory(ProductFactory)
    sku = Sequence(lambda n: f"SKU-{n + 1:04d}")
    price = Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    stock_quantity = Faker("pyint", min_value=0, max_value=100)
    sort_order = None
    is_active = True

    class Meta:
        model = ProductVariant


class ProductImageFactory(DjangoModelFactory):
    product = SubFactory(ProductFactory)
    image = ImageField(filename=Sequence(lambda n: f"product_image_{n + 1}.jpg"))
    alt_text = Faker("word")
    sort_order = None
    is_active = True

    class Meta:
        model = ProductImage
