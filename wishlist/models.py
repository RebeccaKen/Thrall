from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Wishlist(models.Model):
    name = models.CharField(max_length=100, default='Default Name')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.item