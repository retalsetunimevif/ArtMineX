from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from Accounts.forms import LoginForm, AddUserForm
from ArtMineX.models import Image


# Create your views here.


class LoginFormView(View):

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
    def get(self,request):
        user = AddUserForm()
        users = User.objects.order_by('-date_joined')[:3]
        return render(request, 'forms.html', {'form': user, 'list': users})

    def post(self, request):
        user = AddUserForm(request.POST)
        if user.is_valid():
            new_user = user.save(commit=False)
            if user.cleaned_data['password1'] == user.cleaned_data['password2']:
                new_user.set_password(user.cleaned_data.get('password1'))
            new_user.save()
        return redirect('add-user')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('start')


class UserProfileView(View):

    def get(self, request, username):
        access_to_edit = False
        username = User.objects.get(username=username)
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


class EditProfileView(LoginRequiredMixin, View):

    def get(self, request, username):
        if request.user == User.objects.get(username=username):

            return HttpResponse(f'udało się{request.user == User.objects.get(username=username)}')
        else:
            return HttpResponse(f'nie udało się zalogowany "{request.user}", do edycji "{User.objects.get(username=username)}", {request.user == User.objects.get(username=username)}')
