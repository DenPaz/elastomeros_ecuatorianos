from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from model_utils.models import UUIDModel

from apps.core.utils import get_default_image_url

from .utils import product_variant_image_upload_to


class Category(UUIDModel, TimeStampedModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        unique=True,
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
        blank=True,
    )
    sort_order = models.PositiveIntegerField(
        verbose_name=_("Sort order"),
        default=0,
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["sort_order", "name"]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse(
            "products:product_list_by_category",
            kwargs={"category_slug": self.slug},
        )

    def get_image_url(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        return get_default_image_url()


class Attribute(TimeStampedModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
    )
    sort_order = models.PositiveIntegerField(
        verbose_name=_("Sort order"),
        default=0,
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
    )

    class Meta:
        verbose_name = _("Attribute")
        verbose_name_plural = _("Attributes")
        ordering = ["sort_order", "name"]

    def __str__(self):
        return f"{self.name}"


class AttributeValue(TimeStampedModel):
    attribute = models.ForeignKey(
        to=Attribute,
        verbose_name=_("Attribute"),
        related_name="values",
        on_delete=models.CASCADE,
    )
    value = models.CharField(
        verbose_name=_("Value"),
        max_length=255,
    )
    sort_order = models.PositiveIntegerField(
        verbose_name=_("Sort order"),
        default=0,
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
    )

    class Meta:
        verbose_name = _("Attribute value")
        verbose_name_plural = _("Attribute values")
        constraints = [
            models.UniqueConstraint(
                Lower("value"),
                "attribute",
                name="unique_attribute_value",
            ),
        ]
        ordering = ["sort_order", "value"]

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


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
        unique=True,
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
    sort_order = models.PositiveIntegerField(
        verbose_name=_("Sort order"),
        default=0,
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["sort_order", "name"]

    def __str__(self):
        return f"{self.name}"

    def get_min_price(self):
        variants = self.variants.filter(is_active=True)
        if variants.exists():
            return variants.aggregate(models.Min("price"))["price__min"]
        return None

    def get_max_price(self):
        variants = self.variants.filter(is_active=True)
        if variants.exists():
            return variants.aggregate(models.Max("price"))["price__max"]
        return None

    def get_main_image(self):
        first_variant = (
            self.variants.filter(is_active=True).order_by("sort_order").first()
        )
        if first_variant:
            return first_variant.get_default_image()
        return get_default_image_url()


class ProductVariant(UUIDModel, TimeStampedModel):
    product = models.ForeignKey(
        to=Product,
        verbose_name=_("Product"),
        related_name="variants",
        on_delete=models.CASCADE,
    )
    sku = models.CharField(
        verbose_name=_("SKU"),
        max_length=50,
        unique=True,
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    stock = models.PositiveIntegerField(
        verbose_name=_("Stock"),
        default=0,
    )
    attribute_values = models.ManyToManyField(
        to=AttributeValue,
        through="ProductVariantAttributeValue",
        verbose_name=_("Attribute values"),
        related_name="product_variants",
        blank=True,
    )
    sort_order = models.PositiveIntegerField(
        verbose_name=_("Sort order"),
        default=0,
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
    )

    class Meta:
        verbose_name = _("Product variant")
        verbose_name_plural = _("Product variants")
        ordering = ["product", "sort_order", "sku"]

    def __str__(self):
        attribute_values = self.get_attribute_value_display()
        if attribute_values:
            return f"{self.product.name} ({attribute_values})"
        return f"{self.product.name} (SKU: {self.sku})"

    def get_attribute_value_display(self):
        return ", ".join(str(av.value) for av in self.attribute_values.all())

    def get_default_image(self):
        default_image = (
            self.images.filter(is_active=True).order_by("sort_order").first()
        )
        if default_image and default_image.image:
            return default_image.image.url
        return get_default_image_url()


class ProductVariantImage(TimeStampedModel):
    product_variant = models.ForeignKey(
        to=ProductVariant,
        verbose_name=_("Product variant"),
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to=product_variant_image_upload_to,
    )
    alt_text = models.CharField(
        verbose_name=_("Alt text"),
        max_length=255,
        blank=True,
    )
    sort_order = models.PositiveIntegerField(
        verbose_name=_("Sort order"),
        default=0,
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
    )

    class Meta:
        verbose_name = _("Product variant image")
        verbose_name_plural = _("Product variant images")
        ordering = ["product_variant", "sort_order"]

    def __str__(self):
        return f"Image for {self.product_variant}"


class ProductVariantAttributeValue(TimeStampedModel):
    product_variant = models.ForeignKey(
        to=ProductVariant,
        verbose_name=_("Product variant"),
        on_delete=models.CASCADE,
    )
    attribute_value = models.ForeignKey(
        to=AttributeValue,
        verbose_name=_("Attribute value"),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Product variant attribute value")
        verbose_name_plural = _("Product variant attribute values")
        constraints = [
            models.UniqueConstraint(
                fields=["product_variant", "attribute_value"],
                name="unique_product_variant_attribute_value",
            ),
        ]
        ordering = ["product_variant", "attribute_value"]

    def __str__(self):
        return f"{self.product_variant} - {self.attribute_value}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.product_variant_id or not self.attribute_value_id:
            return
        qs = ProductVariantAttributeValue.objects.filter(
            product_variant=self.product_variant,
            attribute_value__attribute=self.attribute_value.attribute,
        )
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError(
                {
                    "attribute_value": _(
                        (
                            "This product variant already has a value for the "
                            "attribute '%(attribute)s'."
                        ),
                    )
                    % {"attribute": self.attribute_value.attribute.name},
                },
            )
