from decimal import Decimal

from django.conf import settings

from apps.products.models import ProductVariant


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, variant: ProductVariant, quantity: int = 1):
        variant_id = str(variant.id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {
                "quantity": 0,
                "price": str(variant.price),
            }
        self.cart[variant_id]["quantity"] += quantity
        self.save()

    def set_quantity(self, variant: ProductVariant, quantity: int):
        variant_id = str(variant.id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {
                "quantity": 0,
                "price": str(variant.price),
            }
        self.cart[variant_id]["quantity"] = quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, variant: ProductVariant):
        variant_id = str(variant.id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def __iter__(self):
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(id__in=variant_ids)
        cart = self.cart.copy()
        for variant in variants:
            cart[str(variant.id)]["variant"] = variant
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
