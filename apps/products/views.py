from django.views.generic import DetailView
from django_filters.views import FilterView

from apps.core.viewmixins import HtmxTemplateMixin

from .filters import ProductFilter
from .models import Product


class ProductListView(HtmxTemplateMixin, FilterView):
    model = Product
    filterset_class = ProductFilter
    template_name = "products/product_list.html"
    htmx_template_name = "#product-grid"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .active()
            .with_images(limit=3)
            .with_price_range()
            .only("id", "name", "slug")
            .order_by("name")
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
