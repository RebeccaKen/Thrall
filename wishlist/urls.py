from django.contrib import admin
from django.urls import path
from . import views
from .views import view_wishlist, add_to_wishlist, remove_from_wishlist, edit_wishlist


urlpatterns = [
    path('wishlist/', view_wishlist, name='view_wishlist'),
    path('add_to_wishlist/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/edit/', edit_wishlist, name='edit_wishlist'),
    path('wishlist/remove/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    ]