from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from products.models import Product
from .forms import WishlistForm


def view_wishlist(request):
    user = request.user

    # Retrieve the wishlist items for the user
    wishlist_items = Wishlist.objects.filter(user=user)

    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})


def add_to_wishlist(request, item_id):
    """Add an item to the wishlist"""
    product = get_object_or_404(Product, pk=item_id)
    user = request.user

    if request.method == 'POST':
        form = WishlistForm(request.POST)
        if form.is_valid():
            size = form.cleaned_data['size']

            wishlist_item = Wishlist.objects.filter(user=user, product=product, size=size)
            if wishlist_item.exists():
                messages.info(request, f'{product.name} ({size}) is already in your wishlist.')
            else:
                # Save the form to create the new wishlist item
                new_wishlist_item = form.save(commit=False)
                new_wishlist_item.user = user
                new_wishlist_item.product = product
                new_wishlist_item.save()
                messages.success(request, f'{product.name} ({size}) has been added to your wishlist.')
        else:
            messages.error(request, 'Invalid request or missing product information.')

    return redirect('view_wishlist')


def remove_from_wishlist(request, item_id):
    """Remove an item from the wishlist"""
    wishlist_item = get_object_or_404(Wishlist, pk=item_id, user=request.user)
    
    if wishlist_item.product is None:
        product_name = "Unknown Product"
    else:
        product_name = wishlist_item.product.name
    
    wishlist_item.delete()
    messages.success(request, f'{product_name} has been removed from your wishlist.')
    return redirect('view_wishlist')