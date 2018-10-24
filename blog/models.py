"""
Models for Blog App
"""
from django.db import models

from users.models import UserProfile


class Post(models.Model):
    """
    Posts Model for Blog
    """
    title = models.CharField(
        'Title',
        max_length=255,
        blank=False,
        help_text='Represents post title.')
    content = models.TextField(
        'Content', blank=False, help_text='Represents post content.')
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_DEFAULT,
        related_name='posts',
        null=True,
        default=None)
    created = models.DateTimeField('Created', auto_now_add=True)
    modified = models.DateTimeField('Modified', auto_now=True)

    class Meta():
        """
        Meta options for Post Model
        """
        ordering = ['id', 'title']

    def __str__(self):
        """
        String Representation Method for Post
        """
        return f'{self.title} - {self.author.profile_name}'
