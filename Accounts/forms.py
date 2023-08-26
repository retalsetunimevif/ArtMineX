from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def empty_email(value):
    """Validation function used to validate that an email field is not empty."""
    if not value:
        raise ValidationError('wypełnij pole email')

def at_symbol_in_email(value):
    """Validation function used to check whether an email address contains the "@" symbol."""
    if not "@" in value:
        raise ValidationError('email must contain "@" sign!')

def empty_password(value):
    """Validation function used to check whether a password field is empty."""
    if not value:
        raise ValidationError('Password can\'t be empty')

class LoginForm(forms.Form):
    """Form class for user login functionality.
    Contains fields for username and password
    input during the login process."""
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)


class AddUserForm(forms.ModelForm):
    """Form class for creating a new user account.
    Includes fields for specifying the username, email,
    and password during user registration."""

    password1 = forms.CharField(widget=forms.PasswordInput,
                                label='password',
                                validators=[empty_password])
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label='re-password',
                                validators=[empty_password])
    email = forms.CharField(validators=[empty_email, at_symbol_in_email])

    class Meta:
        model = User
        fields = ['username', 'email', ]


class UpdateUserAccountForm(forms.ModelForm):
    """Form class for updating user account information.
    Provides fields for modifying user data such as first name,
    last name, and email."""
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email']
