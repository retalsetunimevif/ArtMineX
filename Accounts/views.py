from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View

from Accounts.forms import LoginForm, AddUserForm
from ArtMineX.models import Image


# Create your views here.


class LoginFormView(View):
    """View class for handling user login.
    This view displays the login form and processes user login attempts."""
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'forms.html', {'form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            url = request.GET.get('next', 'start')
            if user is not None:
                login(request, user)
                return redirect(url)
        return render(request, 'forms.html', {'form': login_form})


class AddUserFormView(View):
    """View class for user registration.
    Displays the user registration form
    and handles the creation of new user accounts."""
    def get(self,request):
        if not request.user.is_authenticated:
            user = AddUserForm()
            users = User.objects.order_by('-date_joined')[:3]
            return render(request, 'forms.html', {'form': user, 'list': users})
        return redirect('start')

    def post(self, request):
        user = AddUserForm(request.POST)
        if user.is_valid():
            new_user = user.save(commit=False)
            if user.cleaned_data['password1'] == user.cleaned_data['password2']:
                new_user.set_password(user.cleaned_data.get('password1'))
                new_user.save()
                return redirect('add-user')
        users = User.objects.order_by('-date_joined')[:3]
        return render(request, 'forms.html', {'form': user, 'list': users})


class LogoutView(View):
    """View class to handle user logout. When accessed,
    it logs out the currently authenticated user
    and redirects them to the start page."""
    def get(self, request):
        logout(request)
        return redirect('start')


class UserProfileView(View):
    """View class to display user profiles.
    Handles displaying the profile of a specific user.
    If the user is the profile owner, an 'Edit' option is shown."""
    def get(self, request, username):
        try:
            username = User.objects.get(username=username)
            access_to_edit = False
            if request.user == username:
                access_to_edit = True
            last_images = Image.objects.filter(user=username.id).order_by('-created')[:6]
            top_3_images = Image.objects.filter(user=username.id).order_by('-like')[:3]
            username_as_groups_admin = username.admin_groups.all()
            username_as_group_member = username.member_groups.all()
            return render(request, 'profile.html', {'user_visited': username,
                                                'last_images': [last_images, 'last added'],
                                                'top_3_images': [top_3_images, 'top 3 images'],
                                                'access_to_edit': access_to_edit,
                                                'username_as_groups_admin': [username_as_groups_admin, 'Groups admin'],
                                                'username_as_group_member': [username_as_group_member, 'Groups member'],})
        except User.DoesNotExist:
            return redirect('404')

