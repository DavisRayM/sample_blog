"""
Views for User App
"""
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserProfileRegistrationForm, UserRegistrationForm
from .models import UserProfile
from .tokens import AccountActivationTokenGenerator


def activate(request, uidb64, token):
    """
    Activate Account View
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    # pylint: disable=no-member
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if (user is not None and
            AccountActivationTokenGenerator().check_token(user, token)):
        profile = user.userprofile
        profile.email_confirmed = True
        profile.save()
        login(request, user)
        return redirect('user-profile')
    else:
        return render(request, 'registration/account_activation_invalid.html')


def signup(request):
    """
    Signup View
    """
    # Only Admins and Non-Users Can Signup Users
    if request.user.is_superuser or not request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            profile_form = UserProfileRegistrationForm(request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                # Email Confirmation
                current_site = get_current_site(request)
                subject = 'Activate Your Account'
                message = render_to_string(
                    'registration/account_activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(
                            force_bytes(user.pk)).decode(),
                        'token': AccountActivationTokenGenerator().make_token(
                            user),
                    })
                user.email_user(subject, message)

                # TODO: Redirect to a separate page
                # login(request, user)
                return redirect('home')
        else:
            user_form = UserRegistrationForm()
            profile_form = UserProfileRegistrationForm()

            return render(request, 'users/signup.html', {
                'user_form': user_form,
                'profile_form': profile_form
            })

    return HttpResponseForbidden()


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
