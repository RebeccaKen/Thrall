from django import forms
from django.forms import ModelForm
from .models import Wishlist


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }