from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from products.models import Product
from .forms import WishlistEditForm


def view_wishlist(request):
    user = request.user

    # Retrieve the wishlist items for the user
    wishlist_items = Wishlist.objects.filter(user=user)

    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})


def edit_wishlist(request):
    user = request.user

    # Retrieve the specific wishlist instance for the user
    wishlist = Wishlist.objects.filter(user=user).first()

    if request.method == 'POST':
        form = WishlistEditForm(request.POST, instance=wishlist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wishlist updated successfully.')
            return redirect('view_wishlist')
    else:
        form = WishlistEditForm(instance=wishlist)

    return render(request, 'wishlist/wishlist.html', {'form': form})


def add_to_wishlist(request, item_id):
    """Add an item to the wishlist"""
    product = get_object_or_404(Product, pk=item_id)
    user = request.user
    size = request.POST.get('product_size')

    # Check if the item with the same size already exists in the wishlist for the user
    wishlist_item = Wishlist.objects.filter(user=user, product=product, size=size)
    if wishlist_item.exists():
        messages.info(request, f'{product.name} ({size}) is already in your wishlist.')
    else:
        Wishlist.objects.create(user=user, product=product, size=size)
        messages.success(request, f'{product.name} ({size}) has been added to your wishlist.')

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