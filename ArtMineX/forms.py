from django import forms
from django.contrib.auth.models import User

from ArtMineX.models import Genre, Image, ImageComment, Group


class GenreForm(forms.ModelForm):
    """A form class for handling species genre."""
    class Meta:
        model = Genre
        fields = '__all__'


class ImageForm(forms.ModelForm):
    """A form class for handling images."""
    class Meta:
        model = Image
        fields = ['title', 'description', 'genre', 'image']


class ImageCommentForm(forms.ModelForm):
    """A form class for handling image comments"""
    class Meta:
        model = ImageComment
        fields = ['text']
        labels = {'text': "Comment"}


class GroupForm(forms.ModelForm):
    """A form class to handle group"""
    class Meta:
        model = Group
        fields = ['name']
