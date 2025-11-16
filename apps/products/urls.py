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
        route="<slug:slug>/",
        view=ProductDetailView.as_view(),
        name="product_detail",
    ),
]
