from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist


def view_wishlist(request):
    """A view that renders the wishlist contents page"""
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})

def add_to_wishlist(request, item_id):
    """Add an item to the wishlist"""
    product = get_object_or_404(Product, pk=item_id)
    user = request.user
    size = request.POST.get('product_size')

    # Check if the item with the same size already exists in the wishlist for the user
    wishlist_item = Wishlist.objects.filter(user=user, item=product, size=size)
    if wishlist_item.exists():
        messages.info(request, f'{product.name} ({size}) is already in your wishlist.')
    else:
        Wishlist.objects.create(user=user, item=product, size=size)
        messages.success(request, f'{product.name} ({size}) has been added to your wishlist.')

    return redirect('view_wishlist')

def remove_from_wishlist(request, item_id):
    """Remove an item from the wishlist"""
    wishlist_item = get_object_or_404(Wishlist, pk=item_id, user=request.user)
    product_name = wishlist_item.item.name
    wishlist_item.delete()
    messages.success(request, f'{product_name} has been removed from your wishlist.')
    return redirect('view_wishlist')