from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django.views.generic import View

from apps.products.models import ProductVariant

from .cart import Cart
from .forms import CartAddProductForm


class CartAddView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        variant_id = kwargs.get("variant_id")
        variant = get_object_or_404(ProductVariant, id=variant_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd["override"]:
                cart.set_quantity(variant, cd["quantity"])
                messages.success(request, _("Cart quantity updated."))
            else:
                cart.add(variant, cd["quantity"])
                messages.success(request, _("Item added to cart."))
            return redirect("cart:cart_detail")
        messages.error(request, _("Error adding item to cart."))
        return redirect(
            "products:product_detail",
            kwargs={"slug": variant.product.slug},
        )


class CartRemoveView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        variant_id = kwargs.get("variant_id")
        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart.remove(variant)
        messages.success(request, _("Item removed from cart."))
        return redirect("cart:cart_detail")


class CartDetailView(TemplateView):
    template_name = "cart/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_instance = context.get("cart", Cart(self.request))
        cart_items = [
            {
                **item,
                "update_quantity_form": CartAddProductForm(
                    initial={
                        "quantity": item["quantity"],
                        "override": True,
                    },
                ),
            }
            for item in cart_instance
        ]
        context["cart_items"] = cart_items
        context["cart"] = cart_instance
        return context
