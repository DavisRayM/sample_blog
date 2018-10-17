"""
Admin Configuration for Users App
"""
from django.contrib import admin

from .models import UserProfile

admin.site.register(UserProfile)
