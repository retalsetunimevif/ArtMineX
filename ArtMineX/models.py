from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from thumbnails.fields import ImageField


# Create your models here.

class Genre(models.Model):
    """Model: Represents a genre with a name field."""
    genre = models.CharField(max_length=64)

    def __str__(self):
        return self.genre


class Image(models.Model):
    """Model representing images uploaded by users."""
    title = models.CharField(max_length=128)
    description = models.TextField()
    like = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = ImageField(upload_to='images/')
    slug = models.SlugField(max_length=200, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Function to save the image along with
         its corresponding slug based on the date of creation."""
        if not self.slug:
            self.slug = slugify(self.title + str(self.publish))
        super().save(*args, **kwargs)

    def increment_like(self):
        """Method to increment the 'like' count for the associated image."""
        self.like += 1
        self.save()

    def decrease_like(self):
        """Method to decrease the 'like' count for the associated image."""
        self.like -= 1
        self.save()


class Like(models.Model):
    """Model representing likes given to images."""
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='img_like')
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['image', 'username']


class ImageComment(models.Model):
    """Model representing comments associated with images."""
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='img_comment')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


class Group(models.Model):
    """Model representing a group with its associated attributes."""
    name = models.CharField(max_length=128, unique=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_groups')
    created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, blank=True, related_name='member_groups')
    pending_users = models.ManyToManyField(User, blank=True, related_name='pending_groups')
    image = models.ManyToManyField(Image, related_name='image_groups')

    def __str__(self):
        return self.name

    def save(self):
        """Method to save the admin as a member of the group they own."""
        super().save()
        self.members.add(self.admin)

    # function for admin of group
    def accept_pending_user(self, user):
        """Method for Admin Control Over Pending Users"""
        if user in self.pending_users.all():
            # adding user to member_groups
            self.members.add(user)
            # remove user from pending_groups
            self.pending_users.remove(user)

    def reject_pending_user(self, user):
        """Method for Admin Control to Reject Pending Users"""
        if user in self.pending_users.all():
            # remove user from pending_groups
            self.pending_users.remove(user)
