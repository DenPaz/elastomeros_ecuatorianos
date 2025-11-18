from django.urls import path

from .views import CartAddView
from .views import CartDetailView
from .views import CartRemoveView

app_name = "cart"

urlpatterns = [
    path(
        route="",
        view=CartDetailView.as_view(),
        name="cart_detail",
    ),
    path(
        route="add/<uuid:variant_id>/",
        view=CartAddView.as_view(),
        name="cart_add",
    ),
    path(
        route="remove/<uuid:variant_id>/",
        view=CartRemoveView.as_view(),
        name="cart_remove",
    ),
]
