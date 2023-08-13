from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)


class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='re-password')

    class Meta:
        model = User
        fields = ['username', 'email', ]


class UpdateUserAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email']
