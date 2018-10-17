"""
Module Containing Forms in User
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileRegistrationForm(forms.ModelForm):
    """
    User Profile Registration Form
    """

    class Meta():
        """
        Meta Options for UserProfileRegistrationForm
        """
        model = UserProfile
        fields = ['birth_date', 'bio', 'gender']
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class UserRegistrationForm(UserCreationForm):
    """
    Custom User Registration Form
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)

    class Meta():
        """
        Meta Options for UserRegistrationForm
        """
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password1',
            'password2'
        ]

    def save(self, commit=True):
        """
        Custom save method
        """
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
