from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import AttributesSchema
from .models import Category
from .models import Product
from .models import ProductImage
from .models import ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("General information"),
            {
                "fields": [
                    "id",
                    "name",
                    "slug",
                    "description",
                    "image",
                    "is_active",
                ],
            },
        ),
        (
            _("Timestamps"),
            {
                "classes": ["collapse"],
                "fields": [
                    "created",
                    "modified",
                ],
            },
        ),
    )
    list_display = ["name", "product_count", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}
    readonly_fields = ["id", "created", "modified"]
    show_full_result_count = False
    list_per_page = 20

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.resolver_match.url_name.endswith("_changelist"):
            queryset = queryset.with_product_count(active_only=False)
        return queryset

    @admin.display(description=_("Products"), ordering="_product_count")
    def product_count(self, obj):
        return obj.product_count


@admin.register(AttributesSchema)
class AttributesSchemaAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("General information"),
            {
                "fields": [
                    "id",
                    "name",
                    "schema",
                    "description",
                ],
            },
        ),
        (
            _("Timestamps"),
            {
                "classes": ["collapse"],
                "fields": [
                    "created",
                    "modified",
                ],
            },
        ),
    )
    list_display = ["name", "attributes"]
    search_fields = ["name"]
    readonly_fields = ["id", "created", "modified"]
    show_full_result_count = False
    list_per_page = 20


class ProductVariantInline(admin.StackedInline):
    model = ProductVariant
    extra = 0
    min_num = 1
    ordering = ["sort_order", "sku"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.with_product()


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    ordering = ["sort_order", "id"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.with_product()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline, ProductImageInline]
    fieldsets = (
        (
            _("General information"),
            {
                "fields": [
                    "id",
                    "category",
                    "name",
                    "slug",
                    "short_description",
                    "full_description",
                    "is_active",
                ],
            },
        ),
        (
            _("Timestamps"),
            {
                "classes": ["collapse"],
                "fields": [
                    "created",
                    "modified",
                ],
            },
        ),
    )
    list_display = ["name", "category", "price_range", "total_stock", "is_active"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "slug", "variants__sku"]
    prepopulated_fields = {"slug": ["name"]}
    readonly_fields = ["id", "created", "modified"]
    show_full_result_count = False
    list_per_page = 20

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.resolver_match.url_name.endswith("_changelist"):
            queryset = (
                queryset.with_category()
                .with_price_range(active_only=False)
                .with_total_stock(active_only=False)
            )
        return queryset
