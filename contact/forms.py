from django import forms
from django.forms import ModelForm
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'comments', 'rating']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 5}),
        }
