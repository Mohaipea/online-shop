from django import forms

from shopproducts.models import Product


class OrderForm(forms.Form):
    product_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    quantity = forms.IntegerField(
        widget=forms.NumberInput(),
        initial=1
    )