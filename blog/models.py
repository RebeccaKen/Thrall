from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import math


STATUS = ((0, "Draft"), (1, "Published"))


class Tag(models.Model):
    """
    Model representing a tag for blog posts.

    Attributes:
        name (str): The name of the tag.
        created_on (datetime): The date and time the tag was created.
    """

    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Model representing a blog post.

    Attributes:
        title (str): The title of the blog post.
        slug (str): A unique slug for the blog post's URL.
        author (User): The author of the blog post (foreign key to User model).
        excerpt (str): A brief excerpt or summary of the blog post.
        updated_on (datetime): The date and time the post was last updated.
        content (str): The content or body of the blog post.
        created_on (datetime): The date and time the blog post was created.
        status (int): The status of the blog post (Draft or Published).
        tags (Tag): Many-to-many relationship with Tag model.
        image (ImageField): An optional image associated with the blog post.
        reading_time (int): Estimated reading time for the blog post
        (in minutes).
        likes (User): Many-to-many relationship with User model for post likes.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    image = models.ImageField(null=True, blank=True)
    reading_time = models.PositiveIntegerField(default=0, editable=False)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        word_count = len(self.content.split())
        self.reading_time = math.ceil(word_count / 200)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Model representing a comment on a blog post.

    Attributes:
        post (Post): The blog post this comment is associated with.
        name (str): The name of the commenter.
        email (str): The email address of the commenter.
        body (str): The content of the comment.
        created_on (datetime): The date and time the comment was created.
        approved (bool): Whether the comment is approved or not.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"