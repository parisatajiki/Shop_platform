from .models import DiscountCode

from django import forms


class DiscountCodeForm(forms.Form):
    name = forms.CharField(label='Name', max_length=20,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))