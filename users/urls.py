"""
User App URL Configurations
"""
from django.contrib.auth import views as auth_views
# from django.conf.urls import url
from django.urls import path

from . import views

# TODO: Enable Registration
urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('new/', views.signup, name='user-create'),
    path('profile/', views.profile, name='user-profile'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate,
    #     name='activate'),
]
