# Generated by Django 4.2.4 on 2023-08-07 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ArtMineX', '0002_image_genre_like_imagecomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagecomment',
            old_name='image',
            new_name='comment',
        ),
    ]