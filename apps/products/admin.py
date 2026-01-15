import nested_admin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category
from .models import Product
from .models import ProductVariant
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
                    "is_active",
                ),
            },
        ),
    )
    list_display = ["name", "product_count", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["id", "created", "modified"]
    show_full_result_count = False
    list_per_page = 10

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if all(
            [
                request.resolver_match,
                request.resolver_match.url_name.endswith("changelist"),
            ],
        ):
            queryset = queryset.with_product_counts()
        return queryset

    @admin.display(description=_("Products"), ordering="product_count")
    def product_count(self, obj):
        return getattr(obj, "product_count", 0)


class ProductVariantImageInline(nested_admin.NestedTabularInline):
    model = ProductVariantImage
    extra = 0
    ordering = ["sort_order"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.with_variant()


class ProductVariantInline(nested_admin.NestedTabularInline):
    inlines = [ProductVariantImageInline]
    model = ProductVariant
    extra = 0
    min_num = 1
    ordering = ["sort_order", "sku"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.with_product()


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
                    "short_description",
                    "full_description",
                    "is_active",
                ),
            },
        ),
    )
    list_display = ["name", "category", "price_range", "total_stock", "is_active"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "slug"]
    autocomplete_fields = ["category"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["id", "created", "modified"]
    show_full_result_count = False
    list_per_page = 10

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if all(
            [
                request.resolver_match,
                request.resolver_match.url_name.endswith("changelist"),
            ],
        ):
            queryset = queryset.with_price_range().with_total_stock()
        return queryset

    @admin.display(description=_("Price range"), ordering="min_price")
    def price_range(self, obj):
        min_price = getattr(obj, "min_price", None)
        max_price = getattr(obj, "max_price", None)
        if min_price is None:
            return _("N/A")
        if min_price == max_price:
            return f"${min_price:.2f}"
        return f"${min_price:.2f} - ${max_price:.2f}"

    @admin.display(description=_("Total stock"), ordering="total_stock")
    def total_stock(self, obj):
        return getattr(obj, "total_stock", 0)
