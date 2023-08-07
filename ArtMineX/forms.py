from django import forms

from ArtMineX.models import Genre, Image, ImageComment


class FormGenre(forms.ModelForm):

    class Meta:
        name = Genre
        fields = '__all__'


class FormImage(forms.ModelForm):

    class Meta:
        name = Image
        fields = ['title', 'description']


class FormImageComment(forms.ModelForm):

    class Meta:
        name = ImageComment
        fields = ['text']
        labels = {'text': "Komentarz"}