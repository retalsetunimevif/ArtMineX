from django import forms
from ArtMineX.models import Genre, Image, ImageComment


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
