from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import UUIDModel

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
