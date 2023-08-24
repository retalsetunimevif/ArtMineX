from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def empty_email(value):
    if not value:
        raise ValidationError('wypełnij pole email')

def at_symbol_in_email(value):
    if not "@" in value:
        raise ValidationError('email must contain "@" sign!')

def empty_password(value):
    if not value:
        raise ValidationError('Password can\'t be empty')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)


class AddUserForm(forms.ModelForm):
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
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email']
