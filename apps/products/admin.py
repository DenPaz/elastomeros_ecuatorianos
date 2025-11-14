import nested_admin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Attribute
from .models import AttributeValue
from .models import Category
from .models import Product
from .models import ProductVariant
from .models import ProductVariantAttributeValue
from .models import ProductVariantImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("General information"),
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "image",
                    "sort_order",
                    "is_active",
                ),
            },
        ),
    )
    list_display = ["name", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["id", "created", "modified"]
    list_per_page = 10


class AttributeValueInline(nested_admin.NestedTabularInline):
    model = AttributeValue
    extra = 0
    sortable_field_name = "sort_order"


@admin.register(Attribute)
class AttributeAdmin(nested_admin.NestedModelAdmin):
    inlines = [AttributeValueInline]
    fieldsets = (
        (
            _("General information"),
            {
                "fields": (
                    "name",
                    "description",
                    "sort_order",
                    "is_active",
                ),
            },
        ),
    )
    list_display = ["name", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
    readonly_fields = ["id", "created", "modified"]
    list_per_page = 10


class ProductVariantAttributeValueInline(nested_admin.NestedTabularInline):
    model = ProductVariantAttributeValue
    extra = 0


class ProductVariantImageInline(nested_admin.NestedTabularInline):
    model = ProductVariantImage
    extra = 0
    sortable_field_name = "sort_order"


class ProductVariantInline(nested_admin.NestedTabularInline):
    inlines = [ProductVariantAttributeValueInline, ProductVariantImageInline]
    model = ProductVariant
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("product").prefetch_related(
            "attribute_values",
            "images",
        )


@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductVariantInline]
    fieldsets = (
        (
            _("General information"),
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "description",
                    "sort_order",
                    "is_active",
                ),
            },
        ),
    )
    list_display = ["name", "category", "is_active"]
    list_filter = ["is_active", "category"]
    search_fields = ["name"]
    autocomplete_fields = ["category"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["id", "created", "modified"]
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("category")
