import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Category
from .models import Product


class ProductFilter(django_filters.FilterSet):
    categories = django_filters.ModelMultipleChoiceFilter(
        field_name="category__slug",
        to_field_name="slug",
        queryset=Category.objects.active(),
    )
    ordering = django_filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("min_price", "min_price"),
            ("max_price", "max_price"),
        ),
        choices=(
            ("name", _("A-Z order")),
            ("-name", _("Z-A order")),
            ("min_price", _("Low-High price")),
            ("-min_price", _("High-Low price")),
        ),
        widget=forms.Select,
        empty_label=None,
    )

    class Meta:
        model = Product
        fields = ["categories", "ordering"]
