"""
Module Containing Models for User App
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class UserProfile(models.Model):
    """
    User Profile Model
    """
    GENDER_CHOICES = ((0, _('Other')), (1, _('Male')), (2, _('Female')))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(
        'Birth Date',
        blank=True,
        default=None,
        help_text='Represents User Birth Date.')
    bio = models.TextField(
        'Biography', blank=True, default='Introduction ? Why ?')
    gender = models.IntegerField(
        'Gender', blank=True, default=0, choices=GENDER_CHOICES)
    email_confirmed = models.BooleanField('Email Confirmed', default=False)

    class Meta():
        """
        Meta Options For UserProfile
        """
        ordering = ['id', 'user']

    def __str__(self):
        """
        String Representation Method
        """
        return f'{self.profile_name}\'s Profile'

    @property
    def profile_name(self):
        """
        Returns the full name of the associated User
        """
        return self.user.get_full_name()  # pylint: disable=no-member

    @property
    def gender_display(self):
        """
        Returns Human Readable value for Gender
        """
        return self.get_gender_display()  # pylint: disable=no-member
