from django.db import models
from datetime import date, time

# Create your models here.



class Contact(models.Model):
    """
    The contact model represents the feedback provided by users of the system.
    It contains fields to store the name and email address of the user,
    their comments, the date of the feedback, the rating they gave. 

    Attributes:
       - name (CharField): A required field to store the name of the user
       giving feedback, with a maximum length of 100 characters.
       - email (EmailField): A required field to store the email address of
       the user giving feedback.
       - comments (TextField): A field to store the comments made by the user
       giving feedback.
       - date (DateTimeField): A field to store the date and time the feedback
       was given, with the default value being the current date and time.
       - rating (IntegerField): A field to store the rating given by the user,
       with the available choices being 1 to 5.

    Methods:

        __str__(self): A method that returns a string representation of the
        contact object, consisting of the name of the user and the word
        "Contact".

        get_rating_display(self): A method that returns a formatted string
        representation of the rating, e.g. "3/5".

        save(self, *args, **kwargs): Overrides the default save method to
        set approved to False when a new feedback is created.
    """
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField()
    comments = models.TextField()
    date = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(choices=((1, '1'), (2, '2'),
                                 (3, '3'), (4, '4'), (5, '5')))

    class Meta:
        verbose_name_plural = 'Contact'

    def __str__(self):
        return f"{self.name}'s contact message"

    def get_rating_display(self):
        return f"{self.rating}/5"

    get_rating_display.short_description = 'Rating'

    def save(self, *args, **kwargs):
        self.approved = False
        super().save(*args, **kwargs)
