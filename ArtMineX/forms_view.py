from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from ArtMineX.forms import ImageForm, GenreForm, ImageCommentForm
from ArtMineX.models import Image, Genre


class AddImageFormView(LoginRequiredMixin,View):

    def get(self, request):
        form_image = ImageForm()
        return render(request, 'forms.html', {'form': form_image})

    def post(self, request):
        form_image = ImageForm(request.POST, request.FILES)
        if form_image.is_valid():
            user = request.user
            image = form_image.save(commit=False)
            image.user = user
            image.save()
            url = 'start'
            if request.GET['next']:
                url = request.GET.get('next', 'start')
            return redirect(url)
        return render(request, 'forms.html', {'form': form_image})

class AddGenreFormView(View):
    def get(self, request):
        genre_list = Genre.objects.all()
        form_genre = GenreForm()
        return render(request, 'forms.html', {'form': form_genre, 'list': genre_list})

    def post(self, request):
        form_genre = GenreForm(request.POST)
        if form_genre.is_valid():
            form_genre.save()
        return redirect('add-genre')
