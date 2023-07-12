from django.contrib import admin
from .models import Wishlist

class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )
admin.site.register(Wishlist)