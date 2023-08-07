from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.

class Genre(models.Model):

    genre = models.CharField(max_length=64)

    def __str__(self):
        return self.genre


class Image(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    like = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + str(self.created))
        super().save(*args, **kwargs)
