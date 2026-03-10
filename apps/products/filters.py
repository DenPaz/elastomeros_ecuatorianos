import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Category
from .models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        field_name="category__slug",
        to_field_name="slug",
        queryset=(
            Category.objects.active()
            .with_product_count()
            .only("id", "name", "slug")
            .order_by("name")
        ),
        widget=forms.CheckboxSelectMultiple,
    )
    ordering = django_filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("min_price", "min_price"),
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
        fields = ["category", "ordering"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields["category"].label_from_instance = lambda obj: (
            f"{obj.name} ({obj.product_count})"
        )
