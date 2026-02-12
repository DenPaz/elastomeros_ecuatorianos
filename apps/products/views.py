from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .active()
            .with_active_images(limit=3)
            .with_price_range()
            .only("id", "name", "slug")
            .order_by("name")
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
