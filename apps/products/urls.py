from django.urls import path

from .views import ProductDetailView
from .views import ProductListView

app_name = "products"

urlpatterns = [
    path(
        route="",
        view=ProductListView.as_view(),
        name="product_list",
    ),
    path(
        route="<slug:category_slug>/",
        view=ProductListView.as_view(),
        name="product_list_by_category",
    ),
    path(
        route="<slug:product_slug>/",
        view=ProductDetailView.as_view(),
        name="product_detail",
    ),
]
