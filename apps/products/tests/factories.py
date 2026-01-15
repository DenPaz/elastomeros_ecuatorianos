from django.utils.text import slugify
from factory import Faker
from factory import LazyAttribute
from factory import Sequence
from factory import SubFactory
from factory import Trait
from factory import post_generation
from factory.django import DjangoModelFactory
from factory.django import ImageField

from apps.products.models import Category
from apps.products.models import Product
from apps.products.models import ProductVariant
from apps.products.models import ProductVariantImage


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
            ProductFactory(category=self)


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
            ProductVariantFactory(product=self)


class ProductVariantFactory(DjangoModelFactory):
    product = SubFactory(ProductFactory)
    sku = Sequence(lambda n: f"SKU-{n:05d}")
    price = Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    stock_quantity = Faker("pyint", min_value=0, max_value=100)
    attributes = Sequence(lambda n: {"attribute": f"value_{n + 1}"})
    sort_order = None
    is_active = True

    class Meta:
        model = ProductVariant
        skip_postgeneration_save = True

    @post_generation
    def images(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        for _ in range(extracted):
            ProductVariantImageFactory(variant=self)


class ProductVariantImageFactory(DjangoModelFactory):
    variant = SubFactory(ProductVariantFactory)
    image = ImageField(filename=Sequence(lambda n: f"variant_image_{n + 1}.jpg"))
    alt_text = Faker("sentence")
    sort_order = None
    is_active = True

    class Meta:
        model = ProductVariantImage
