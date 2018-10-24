"""
Module Containing Forms In Blog
"""
from django import forms


class ContactForm(forms.Form):
    """
    Contact Me Form
    """
    contact_name = forms.CharField(required=True)
    contact_name.widget = forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name'})
    contact_email = forms.EmailField(required=True)
    contact_email.widget = forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'})
    email_subject = forms.CharField(required=True)
    email_subject.widget = forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Subject'}
    )
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Message'}),
        required=True)

    class Meta():
        """
        Meta Options For ContactForm
        """
        fields = ['contact_name', 'contact_email', 'content']
