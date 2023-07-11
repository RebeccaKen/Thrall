from django.contrib import admin
from django.urls import path
from .views import view_wishlist, add_to_wishlist, remove_from_wishlist

urlpatterns = [
    path('wishlist/', view_wishlist, name='view_wishlist'),
    path('wishlist/add/<int:item_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),]