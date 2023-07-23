from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Model representing a category for products.

    Attributes:
        name (str): The name of the category.
        friendly_name (str): A user-friendly name for the category (optional).

    Methods:
        __str__(): Returns a string representation of the category name.
        get_friendly_name(): Returns the friendly name of the category.
    """
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """
    Model representing a product.

    Attributes:
        category (Category): The category to which the product belongs (foreign key to Category model).
        name (str): The name of the product.
        sku (str): A unique SKU (Stock Keeping Unit) for the product (optional).
        description (str): The description of the product.
        has_sizes (bool): Indicates if the product has sizes (optional).
        price (Decimal): The price of the product.
        rating (Decimal): The rating of the product (optional).
        image_url (str): The URL of the product image (optional).
        image (ImageField): An optional image file for the product.

    Methods:
        __str__(): Returns a string representation of the product name.
    """
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    sku = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(default=True)
    has_sizes = models.BooleanField(default=True, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Model representing a review for a product.

    Attributes:
        product (Product): The product associated with this review (foreign key
        to Product model).
        user (User): The user who wrote the review (foreign key to User model).
        score (int): The numerical score given to the product in the review (1
        to 5).
        comment (str): The comment or feedback provided in the review.
        date_created (datetime): The date and time when the review was created
        (auto-generated).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)