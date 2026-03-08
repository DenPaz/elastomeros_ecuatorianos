from django.utils.text import slugify
from factory import Faker
from factory import LazyAttribute
from factory import Sequence
from factory import SubFactory
from factory import Trait
from factory import post_generation
from factory.django import DjangoModelFactory
from factory.django import ImageField
from factory.fuzzy import FuzzyChoice

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
                filename=Sequence(lambda n: f"category_{n + 1}.jpg"),
            ),
        )

    @post_generation
    def products(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        if isinstance(extracted, int):
            ProductFactory.create_batch(extracted, category=self, **kwargs)
        elif isinstance(extracted, list):
            for overrides in extracted:
                ProductFactory(category=self, **{**kwargs, **overrides})
        else:
            return


def build_schema(index: int, n_attributes: int) -> dict:
    schema = {
        "type": "object",
        "title": f"Attributes schema {index}",
        "required": ["type"],
        "properties": {
            "type": {
                "type": "string",
                "const": f"attributes_schema_{index}",
                "widget": "hidden",
                "readonly": True,
            },
        },
        "additionalProperties": False,
    }
    for i in range(1, n_attributes + 1):
        attribute_key = f"attribute_{i}"
        schema["properties"][attribute_key] = {
            "type": "string",
            "title": f"Attribute {i}",
        }
        schema["required"].append(attribute_key)
    return schema


class AttributesSchemaFactory(DjangoModelFactory):
    index = Sequence(lambda n: n + 1)
    n_attributes = Faker("pyint", min_value=1, max_value=3)

    name = LazyAttribute(lambda obj: f"Attributes schema {obj.index}")
    schema = LazyAttribute(lambda obj: build_schema(obj.index, obj.n_attributes))
    description = Faker("paragraph")

    class Meta:
        model = AttributesSchema
        exclude = ["index", "n_attributes"]


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
        schema = kwargs.pop("attributes_schema", None) or AttributesSchemaFactory()
        if isinstance(extracted, int):
            ProductVariantFactory.create_batch(
                extracted,
                product=self,
                attributes_schema=schema,
                **kwargs,
            )
        elif isinstance(extracted, list):
            for overrides in extracted:
                ProductVariantFactory(
                    product=self,
                    attributes_schema=schema,
                    **{**kwargs, **overrides},
                )
        else:
            return

    @post_generation
    def images(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        if isinstance(extracted, int):
            ProductImageFactory.create_batch(extracted, product=self, **kwargs)
        elif isinstance(extracted, list):
            for overrides in extracted:
                ProductImageFactory(product=self, **{**kwargs, **overrides})
        else:
            return


def build_attributes_from_schema(schema: dict, sku: str) -> dict:
    properties = schema.get("properties", {})
    type_const = properties.get("type", {}).get("const")
    attributes = {"type": type_const} if type_const else {}
    keys = sorted(k for k in properties if k != "type")
    for i, key in enumerate(keys, start=1):
        attributes[key] = f"Value {i} ({sku})"
    return attributes


class ProductVariantFactory(DjangoModelFactory):
    attributes_schema = SubFactory(AttributesSchemaFactory)

    product = SubFactory(ProductFactory)
    sku = Sequence(lambda n: f"SKU-{n + 1:04d}")
    attributes = LazyAttribute(
        lambda obj: build_attributes_from_schema(obj.attributes_schema.schema, obj.sku),
    )
    price = Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    stock = Faker("pyint", min_value=0, max_value=100)
    is_active = True

    class Meta:
        model = ProductVariant
        exclude = ["attributes_schema"]


class ProductImageFactory(DjangoModelFactory):
    product = SubFactory(ProductFactory)
    image = ImageField(
        filename=Sequence(lambda n: f"product_image_{n + 1}.jpg"),
        width=Faker("pyint", min_value=100, max_value=800),
        height=Faker("pyint", min_value=100, max_value=800),
        color=FuzzyChoice(
            ["red", "green", "blue", "yellow", "purple", "orange", "black"],
        ),
    )
    alt_text = Faker("word")
    is_active = True

    class Meta:
        model = ProductImage
