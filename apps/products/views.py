from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView

from apps.core.viewmixins import HtmxTemplateMixin

from .models import Category
from .models import Product


class ProductListView(HtmxTemplateMixin, ListView):
    model = Product
    template_name = "products/product_list.html"
    htmx_template_name = "#products-list"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .active()
            .with_category()
            .with_variants_and_images()
            .with_price_range()
            .order_by("name")
        )

        category_slug = self.request.GET.get("category")
        search_query = self.request.GET.get("q", "")

        self.category = None
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["categories"] = (
            Category.objects.active()
            .with_products_count()
            .only("id", "name", "slug")
        )
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
