'''
Description:
This Django code defines the models for a basic social networking application, including User, Post, and Profile.

1. The `User` model extends Django's `AbstractUser` model to customize user authentication and includes default 
fields like username, password, email, etc.

2. The `Post` model represents a post in the application, containing fields for content, author 
(a ForeignKey to the User model), and timestamp.

3. The `Profile` model stores additional information about users, including their followers and following relationships. 
It has a one-to-one relationship with the User model and includes ManyToMany relationships with other users for followers 
and following.

These models provide the foundation for storing user data, posts, and relationships in the social networking application.
'''

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.timestamp}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followers')
    following = models.ManyToManyField(User, related_name='following')

