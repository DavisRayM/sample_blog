"""
Views for Blog App
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ContactForm
from .models import Post


def about(request):
    """
    About Page View
    """
    return render(request, 'blog/about.html')


def contact(request):
    """
    Contact Us Page View
    """
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name')
            contact_email = request.POST.get('contact_email')
            form_content = request.POST.get('content', '')
            email_subject = request.POST.get('email_subject', '')

            template = get_template('blog/contact_template.txt')
            context = {
                'name': contact_name,
                'subject': email_subject,
                'content': form_content
            }

            content = template.render(context)

            email = EmailMessage(
                email_subject, content,
                to=['davisraymondmuro@outlook.com'],
                headers={'Reply-To': contact_email})

            email.send()
            return redirect('contact-page')
    else:
        return render(request, 'blog/contact.html', {'form': form_class})


class PostDetailView(DetailView):
    """
    Post Detail View
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    """
    Post Create View
    """
    model = Post
    redirect_field_name = 'redirect_to'
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def test_func(self):
        """
        Test Function
        """
        try:
            profile = self.request.user.userprofile
            return profile.email_confirmed
        # pylint: disable=no-member
        except (User.DoesNotExist, AttributeError):
            if self.request.user.is_superuser:
                return True
            return False

    def form_valid(self, form):
        """
        Custom form_valid method
        """
        post = form.save(commit=False)
        post.author = self.request.user.userprofile
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
        if post.author != self.request.user.userprofile:
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

        if post.author != user.userprofile and user.is_superuser:
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
