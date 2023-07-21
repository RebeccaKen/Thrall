from django import forms
from .models import Wishlist

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['name', 
                  'description', 
                  'size', 
                  'price', 
                  'rating', 
                  'image_url', 
                  'image', 
                  'product'
                  ]