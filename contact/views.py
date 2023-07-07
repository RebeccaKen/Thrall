from django.shortcuts import render
from .models import Contact

# Create your views here.

def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'contact_list.html', {'contacts': contacts})