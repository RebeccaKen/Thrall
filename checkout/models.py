import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    """
    Model representing an order made by a user.

    Attributes:
        order_number (str): A unique identifier for the order (auto-generated).
        user_profile (UserProfile): The user profile associated with the order.
        full_name (str): The full name of the user placing the order.
        email (str): The email address of the user.
        phone_number (str): The phone number of the user.
        country (CountryField): The country where the order is being shipped.
        postcode (str): The postcode of the delivery address (optional).
        town_or_city (str): The town or city of the delivery address.
        street_address1 (str): The first line of the delivery address.
        street_address2 (str): The second line of the delivery address (optional).
        county (str): The county of the delivery address (optional).
        date (datetime): The date and time when the order was created (auto-generated).
        delivery_cost (Decimal): The cost of delivery for the order.
        order_total (Decimal): The total cost of the order (excluding delivery).
        grand_total (Decimal): The grand total cost of the order (including delivery).
        original_bag (str): A serialized representation of the user's shopping bag.
        stripe_pid (str): The ID of the payment intent on Stripe.

    Methods:
        _generate_order_number(): Generates a unique order number using UUID4.
        update_total(): Updates the order total, delivery cost, and grand total based on line items.
        save(*args, **kwargs): Overrides the default save method to set the order number if not provided.
        __str__(): Returns a string representation of the order.
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def update_total(self):
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    Model representing an order made by a user.

    Attributes:
        order_number (str): A unique identifier for the order (auto-generated).
        user_profile (UserProfile): The user profile associated with the order.
        full_name (str): The full name of the user placing the order.
        email (str): The email address of the user.
        phone_number (str): The phone number of the user.
        country (CountryField): The country where the order is being shipped.
        postcode (str): The postcode of the delivery address (optional).
        town_or_city (str): The town or city of the delivery address.
        street_address1 (str): The first line of the delivery address.
        street_address2 (str): The second line of the delivery address (optional).
        county (str): The county of the delivery address (optional).
        date (datetime): The date and time when the order was created (auto-generated).
        delivery_cost (Decimal): The cost of delivery for the order.
        order_total (Decimal): The total cost of the order (excluding delivery).
        grand_total (Decimal): The grand total cost of the order (including delivery).
        original_bag (str): A serialized representation of the user's shopping bag.
        stripe_pid (str): The ID of the payment intent on Stripe.

    Methods:
        _generate_order_number(): Generates a unique order number using UUID4.
        update_total(): Updates the order total, delivery cost, and grand total based on line items.
        save(*args, **kwargs): Overrides the default save method to set the order number if not provided.
        __str__(): Returns a string representation of the order.
    """
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'