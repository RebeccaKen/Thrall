from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    Model representing a user profile.

    Attributes:
        user (User): The associated user (foreign key to User model).
        default_phone_number (str): The default phone number for the user (optional).
        default_street_address1 (str): The first line of the default street address (optional).
        default_street_address2 (str): The second line of the default street address (optional).
        default_town_or_city (str): The default town or city for the user (optional).
        default_postcode (str): The default postcode for the user (optional).
        default_county (str): The default county for the user (optional).
        default_country (CountryField): The default country for the user (optional).

    Methods:
        __str__(): Returns a string representation of the user's username.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
