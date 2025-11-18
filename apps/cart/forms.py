from django import forms
from django.utils.translation import gettext_lazy as _


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label=_("Quantity"),
        widget=forms.NumberInput(),
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput(),
    )
