from decimal import Decimal

from django.contrib.postgres.indexes import GinIndex
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONField
from model_utils.models import TimeStampedModel
from model_utils.models import UUIDModel

from apps.core.fields import OrderField
from apps.core.utils import get_default_image_url
from apps.core.validators import FileSizeValidator

from .managers import AttributesSchemaManager
from .managers import CategoryManager
from .managers import ProductImageManager
from .managers import ProductManager
from .managers import ProductVariantManager
from .utils import get_attributes_schema
from .utils import get_default_attributes_schema
from .utils import get_product_image_upload_path


class Category(UUIDModel, TimeStampedModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to="products/categories/",
        validators=[
            FileSizeValidator(max_size=5, unit="MB"),
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
        ],
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        indexes = [
            models.Index(fields=["is_active", "name"]),
        ]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_category_name_case_insensitive",
            ),
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    def get_image_url(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        return get_default_image_url()


class Product(UUIDModel, TimeStampedModel):
    category = models.ForeignKey(
        to=Category,
        verbose_name=_("Category"),
        related_name="products",
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        max_length=255,
        unique=True,
    )
    short_description = models.TextField(
        verbose_name=_("Short description"),
        blank=True,
    )
    full_description = models.TextField(
        verbose_name=_("Full description"),
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
    )

    objects = ProductManager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        indexes = [
            models.Index(fields=["is_active", "name"]),
        ]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "category",
                name="unique_product_name_per_category_case_insensitive",
            ),
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class AttributesSchema(UUIDModel, TimeStampedModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
    )
    schema = models.JSONField(
        verbose_name=_("Schema"),
        default=dict,
    )

    objects = AttributesSchemaManager()

    class Meta:
        verbose_name = _("Attributes schema")
        verbose_name_plural = _("Attributes schemas")
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_attributes_schema_name_case_insensitive",
            ),
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    @property
    def attributes(self):
        schema = self.schema or {}
        properties = schema.get("properties", {})
        attrs = [
            value.get("title", key)
            for key, value in properties.items()
            if key != "type"
        ]
        return sorted(attrs, key=str.casefold)


class ProductVariant(UUIDModel, TimeStampedModel):
    product = models.ForeignKey(
        to=Product,
        verbose_name=_("Product"),
        related_name="variants",
        on_delete=models.CASCADE,
    )
    sku = models.CharField(
        verbose_name=_("SKU"),
        max_length=100,
        unique=True,
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    stock_quantity = models.PositiveIntegerField(
        verbose_name=_("Stock quantity"),
        default=0,
    )
    attributes = JSONField(
        verbose_name=_("Attributes"),
        default=get_default_attributes_schema,
        schema=get_attributes_schema,
    )
    sort_order = OrderField(
        verbose_name=_("Sort order"),
        for_fields=["product"],
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
    )

    objects = ProductVariantManager()

    class Meta:
        verbose_name = _("Product variant")
        verbose_name_plural = _("Product variants")
        indexes = [
            models.Index(fields=["is_active", "sku"]),
            GinIndex(fields=["attributes"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "attributes"],
                name="unique_attributes_per_product_variant",
            ),
        ]
        ordering = ["product", "sort_order", "sku"]

    def __str__(self):
        return f"{self.product.name} (SKU: {self.sku})"


class ProductImage(UUIDModel, TimeStampedModel):
    product = models.ForeignKey(
        to=Product,
        verbose_name=_("Product"),
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to=get_product_image_upload_path,
        validators=[
            FileSizeValidator(max_size=5, unit="MB"),
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
        ],
    )
    alt_text = models.CharField(
        verbose_name=_("Alt text"),
        max_length=255,
        blank=True,
    )
    sort_order = OrderField(
        verbose_name=_("Sort order"),
        for_fields=["product"],
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
    )

    objects = ProductImageManager()

    class Meta:
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")
        indexes = [
            models.Index(fields=["is_active", "product"]),
        ]
        ordering = ["product", "sort_order"]

    def __str__(self):
        return f"Image for {self.product.name} (ID: {self.id})"
