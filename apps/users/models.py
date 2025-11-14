from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from model_utils.models import UUIDModel
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.choices import Gender
from apps.core.choices import Province
from apps.core.validators import FileSizeValidator

from .managers import UserManager
from .utils import get_default_profile_picture_url
from .utils import get_user_upload_path


class User(UUIDModel, AbstractUser):
    first_name = models.CharField(
        verbose_name=_("First name"),
        max_length=100,
    )
    last_name = models.CharField(
        verbose_name=_("Last name"),
        max_length=100,
    )
    email = models.EmailField(
        verbose_name=_("Email address"),
        unique=True,
    )
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.get_full_name()} <{self.email}>"


class UserProfile(UUIDModel):
    user = models.OneToOneField(
        to=User,
        verbose_name=_("User"),
        related_name="profile",
        on_delete=models.CASCADE,
    )
    profile_picture = models.ImageField(
        verbose_name=_("Profile picture"),
        upload_to=get_user_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            FileSizeValidator(max_size=5, unit="MB"),
        ],
        blank=True,
        help_text=_("Maximum size: 5MB. Allowed formats: .jpg, .jpeg, .png"),
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Phone number"),
        blank=True,
    )
    language_preference = models.CharField(
        verbose_name=_("Language preference"),
        max_length=10,
        choices=settings.LANGUAGES,
        default="es",
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=10,
        choices=Gender.choices,
        default=Gender.OTHER,
    )

    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("User profiles")
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self):
        return f"{self.user}"

    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, "url"):
            return self.profile_picture.url
        return get_default_profile_picture_url()


class Address(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(
        to=User,
        verbose_name=_("User"),
        related_name="addresses",
        on_delete=models.CASCADE,
    )
    province = models.CharField(
        verbose_name=_("Province"),
        max_length=50,
        choices=Province.choices,
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=50,
    )
    neighborhood = models.CharField(
        verbose_name=_("Neighborhood"),
        max_length=50,
    )
    street = models.CharField(
        verbose_name=_("Street"),
        max_length=255,
    )
    number = models.CharField(
        verbose_name=_("Number"),
        max_length=20,
        blank=True,
    )
    complement = models.CharField(
        verbose_name=_("Complement"),
        max_length=255,
        blank=True,
    )
    is_default_shipping = models.BooleanField(
        verbose_name=_("Default shipping address"),
        default=False,
    )
    is_default_billing = models.BooleanField(
        verbose_name=_("Default billing address"),
        default=False,
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        ordering = ["user", "-created"]

    def __str__(self):
        return f"{self.user}: {self.full_address}"

    def save(self, *args, **kwargs):
        if self.is_default_shipping:
            Address.objects.filter(
                user=self.user,
                is_default_shipping=True,
            ).exclude(pk=self.pk).update(is_default_shipping=False)
        if self.is_default_billing:
            Address.objects.filter(
                user=self.user,
                is_default_billing=True,
            ).exclude(pk=self.pk).update(is_default_billing=False)
        super().save(*args, **kwargs)

    @property
    def full_address(self):
        parts = [
            self.street,
            f"Nº {self.number}" if self.number else "",
            self.complement,
            self.neighborhood,
            self.city,
            self.get_province_display(),
        ]
        return ", ".join(part for part in parts if part)
