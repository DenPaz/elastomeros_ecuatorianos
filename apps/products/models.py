from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from model_utils.models import UUIDModel


class Category(UUIDModel, TimeStampedModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to="store/category/images/",
        blank=True,
    )

    class Meta:
        verbose_name = _("Product category")
        verbose_name_plural = _("Product categories")
        ordering = ["name"]
