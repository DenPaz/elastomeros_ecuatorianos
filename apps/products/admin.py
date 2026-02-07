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
    list_display = ["name", "products_count", "is_active"]
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
                request.resolver_match.url_name.endswith("_changelist"),
            ],
        ):
            queryset = queryset.with_products_count()
        return queryset

    @admin.display(description=_("Products"), ordering="products_count")
    def products_count(self, obj):
        return getattr(obj, "products_count", 0)


@admin.register(AttributesSchema)
class AttributesSchemaAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("General information"),
            {
                "fields": (
                    "name",
                    "schema",
                ),
            },
        ),
    )
    list_display = ["name", "attributes"]
    search_fields = ["name"]
    readonly_fields = ["id", "created", "modified"]
    show_full_result_count = False
    list_per_page = 10


class ProductVariantInline(admin.TabularInline):
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
    ordering = ["sort_order"]

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
    list_display = [
        "name",
        "category",
        "price_range",
        "total_stock_quantity",
        "is_active",
    ]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "slug", "variants__sku"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["id", "created", "modified"]
    show_full_result_count = False
    list_per_page = 10

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if all(
            [
                request.resolver_match,
                request.resolver_match.url_name.endswith("_changelist"),
            ],
        ):
            queryset = queryset.with_price_range().with_total_stock_quantity()
        return queryset

    @admin.display(description=_("Price range"), ordering="min_price")
    def price_range(self, obj):
        min_price = getattr(obj, "min_price", None)
        max_price = getattr(obj, "max_price", None)
        if min_price is None or max_price is None:
            return _("N/A")
        if min_price == max_price:
            return f"${min_price:.2f}"
        return f"${min_price:.2f} - ${max_price:.2f}"

    @admin.display(description=_("Total stock"), ordering="total_stock_quantity")
    def total_stock_quantity(self, obj):
        return getattr(obj, "total_stock_quantity", 0)
