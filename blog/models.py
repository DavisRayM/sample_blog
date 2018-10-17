"""
Models for Blog App
"""
from django.contrib.auth.models import User
from django.db import models


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
        User,
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
        return f'{self.title} - {self.author_name}'

    @property
    def author_name(self):
        """
        Returns the Full Name of the Posts Author
        """
        try:
            return self.author.get_full_name()  # pylint: disable=no-member
        except AttributeError:
            return 'Anonymous'
