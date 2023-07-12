from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from products.models import Product


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
    wishlist_item = Wishlist.objects.filter(user=user, product=product, size=size)
    if wishlist_item.exists():
        messages.info(request, f'{product.name} ({size}) is already in your wishlist.')
    else:
        Wishlist.objects.create(user=user, product=product, size=size)
        messages.success(request, f'{product.name} ({size}) has been added to your wishlist.')

    return redirect('view_wishlist')


def adjust_wishlist(request, item_id):

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    wishlist = request.session.get('wishlist', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your wishlist')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {wishlist[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your wishlist')

    request.session['wishlist'] = wishlist
    return redirect(reverse('view_wishlist'))


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