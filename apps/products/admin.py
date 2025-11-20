import nested_admin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Attribute
from .models import AttributeValue
from .models import Category
from .models import Product
from .models import ProductImage
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


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ["value", "attribute", "is_active"]
    list_filter = ["attribute", "is_active"]
    search_fields = ["value", "attribute__name"]
    autocomplete_fields = ["attribute"]
    readonly_fields = ["id", "created", "modified"]

    def has_module_permission(self, request):
        return False


class AttributeValueInline(nested_admin.NestedTabularInline):
    model = AttributeValue
    extra = 0
    min_num = 1


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
    autocomplete_fields = ["attribute_value"]

    def get_queryset(self, request):
        return super().get_queryset(request).with_related_fields()


@admin.register(ProductVariant)
class ProductVariantAdmin(nested_admin.NestedModelAdmin):
    list_display = ["product", "sku", "price", "stock"]
    search_fields = ["sku", "product__name"]

    def has_module_permission(self, request):
        return False


class ProductVariantInline(nested_admin.NestedTabularInline):
    inlines = [ProductVariantAttributeValueInline]
    model = ProductVariant
    extra = 0
    min_num = 1


class ProductImageInline(nested_admin.NestedTabularInline):
    model = ProductImage
    extra = 0
    autocomplete_fields = ["product_variant"]


@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductVariantInline, ProductImageInline]
    fieldsets = (
        (
            _("General information"),
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "is_active",
                ),
            },
        ),
        (
            _("Descriptions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "short_description",
                    "full_description",
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
