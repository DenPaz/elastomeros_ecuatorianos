from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Category
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related("category")
        self.category = None
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            self.category = get_object_or_404(
                Category,
                slug=category_slug,
                is_active=True,
            )
            queryset = queryset.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = getattr(self, "category", None)
        context["categories"] = Category.objects.filter(is_active=True)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related(
                "variants",
                "variants__attribute_values",
                "variants__images",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(is_active=True)
        return context
