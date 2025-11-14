import nested_admin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Attribute
from .models import AttributeValue
from .models import Category
from .models import Product
from .models import ProductVariant
from .models import ProductVariantAttributeValue


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


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
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
    extra = 1


class ProductVariantInline(nested_admin.NestedTabularInline):
    inlines = [ProductVariantAttributeValueInline]
    model = ProductVariant
    extra = 1


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
