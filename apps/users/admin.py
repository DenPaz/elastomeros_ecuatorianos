from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms_admin import UserAdminChangeForm
from .forms_admin import UserAdminCreationForm
from .forms_allauth import UserPasswordResetForm
from .models import Address
from .models import User
from .models import UserProfile

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)


admin.site.register(Address)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = "user"
    verbose_name = _("Profile information")
    can_delete = False


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    inlines = [UserProfileInline]
    actions = ["send_password_reset_email"]
    fieldsets = (
        (
            _("Account information"),
            {
                "fields": (
                    "id",
                    "first_name",
                    "last_name",
                    "email",
                    "password",
                    "is_active",
                    "last_login",
                    "date_joined",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            _("Account information"),
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                ),
            },
        ),
    )
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    list_filter = [
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    filter_horizontal = [
        "user_permissions",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "email",
    ]
    ordering = [
        "first_name",
        "last_name",
    ]
    readonly_fields = [
        "id",
        "last_login",
        "date_joined",
    ]
    list_per_page = 10

    @admin.action(description=_("Send password reset email"))
    def send_password_reset_email(self, request, queryset):
        for user in queryset:
            form = UserPasswordResetForm(data={"email": user.email})
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                )
                self.message_user(
                    request,
                    _("Password reset email sent to %(email)s") % {"email": user.email},
                    messages.SUCCESS,
                )
            else:
                self.message_user(
                    request,
                    _("Failed to send password reset email to %(email)s")
                    % {"email": user.email},
                    messages.ERROR,
                )
