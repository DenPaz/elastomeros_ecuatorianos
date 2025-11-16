from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from django.db.models import Prefetch
from django.db.models import Q
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import AttributeValue
from .models import Category
from .models import Product
from .models import ProductVariant
from .models import ProductVariantImage


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
