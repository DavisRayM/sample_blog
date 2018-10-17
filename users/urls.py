"""
User App URL Configurations
"""
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('new/', views.signup, name='user-create'),
    path('profile/', views.profile, name='user-profile')
]
