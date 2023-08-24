from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, redirect
from ArtMineX.forms import ImageForm, GenreForm, ImageCommentForm
from ArtMineX.models import Image, Genre, Group


class AddImageFormView(LoginRequiredMixin,View):

    def get(self, request):
        form_image = ImageForm()
        logged_user = User.objects.get(pk=request.user.id)
        groups_of_logged_user = False
        if logged_user.member_groups.all():
            groups_of_logged_user = logged_user.member_groups.all()
        return render(request, 'forms.html', {'form': form_image,
                                              'groups_of_logged_user': groups_of_logged_user})

    def post(self, request):
        form_image = ImageForm(request.POST, request.FILES)
        if form_image.is_valid():
            user = request.user
            image = form_image.save(commit=False)
            image.user = user
            image.save()
            if request.POST.getlist('selected_groups'):
                selected_groups = request.POST.getlist('selected_groups')
                print(selected_groups)
                for id_group in selected_groups:
                    group = Group.objects.get(pk=id_group)
                    group.image.add(image)
                    group.save()
            url = 'start'
            if 'next' in request.GET:
                url = request.GET.get('next')
            return redirect(url)
        return render(request, 'forms.html', {'form': form_image})

class AddGenreFormView(LoginRequiredMixin, View):
    def get(self, request):
        genre_list = Genre.objects.all()
        form_genre = GenreForm()
        return render(request, 'forms.html', {'form': form_genre, 'list': genre_list})

    def post(self, request):
        form_genre = GenreForm(request.POST)
        if form_genre.is_valid():
            form_genre.save()
        return redirect('add-genre')
