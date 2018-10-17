"""
Views for User App
"""
from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import UserProfileRegistrationForm, UserRegistrationForm
from .models import UserProfile


def signup(request):
    """
    Signup View
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileRegistrationForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileRegistrationForm()
    return render(request, 'users/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def profile(request):
    """
    Profile View :
        Returns Logged In Users Profile
    """
    if request.user.is_authenticated:
        try:
            # pylint: disable=no-member
            profile = request.user.userprofile
            return render(request, 'users/profile.html', {'profile': profile})
        except UserProfile.DoesNotExist:
            raise Http404('Profile Does Not Exist')
    else:
        return redirect('login')
