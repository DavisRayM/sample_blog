"""
Blog App URL Configurations
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path(
        'posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path(
        'posts/<int:pk>/edit',
        views.PostUpdateView.as_view(),
        name='post-update'),
    path(
        'posts/<int:pk>/delete',
        views.PostCreateView.as_view(),
        name='post-delete')
]
