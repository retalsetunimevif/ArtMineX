from django import forms
from django.contrib.auth.models import User

from ArtMineX.models import Genre, Image, ImageComment, Group


class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = '__all__'


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['title', 'description', 'genre', 'image']


class ImageCommentForm(forms.ModelForm):

    class Meta:
        model = ImageComment
        fields = ['text']
        labels = {'text': "Comment"}


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name']
