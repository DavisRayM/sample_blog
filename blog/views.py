"""
Views for Blog App
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Post


class PostDetailView(DetailView):
    """
    Post Detail View
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Post Create View
    """
    model = Post
    redirect_field_name = 'redirect_to'
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        """
        Custom form_valid method
        """
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return HttpResponseRedirect(self.get_success_url(post.id))

    def get_success_url(self, pk):
        """
        Custom get_success_url method
        """
        return reverse_lazy('post-detail', kwargs={'pk': pk})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    Post Update View
    """
    model = Post
    redirect_field_name = 'redirect_to'
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def dispatch(self, request, *args, **kwargs):
        """
        Custom dispatch method
        """
        post = self.get_object()

        # Only the author of the Post is able to edit the Post
        if post.author != self.request.user:
            return HttpResponseForbidden
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """
        Custom get_success_url
        """
        post = self.get_object()
        return reverse_lazy('post-detail', kwargs={'pk': post.id})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    Post Delete View
    """
    model = Post
    template_name = 'blog/post_delete.html'
    redirect_field_name = 'redirect_to'
    context_object_name = 'post'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        """
        Custom dispatch method
        """
        post = self.get_object()
        user = self.request.user

        if post.author != user and user.is_superuser:
            return HttpResponseForbidden
        return super().dispatch(request, *args, **kwargs)


class PostListView(ListView):
    """
    Post List View
    """
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 20
    context_object_name = 'posts'

    def get_queryset(self):
        """
        Custom get_queryset method
        """
        return Post.objects.order_by('-modified')  # pylint: disable=no-member
