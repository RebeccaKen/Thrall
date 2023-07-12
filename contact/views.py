from django.shortcuts import render
from .models import Contact
from .forms import ContactForm
from django.shortcuts import render, redirect


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, 'Your contact form have been sent.')
            return redirect('thrall')
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact_form.html', {'form': form})
