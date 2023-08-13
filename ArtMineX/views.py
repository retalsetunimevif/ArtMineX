from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from ArtMineX.forms import ImageCommentForm
from ArtMineX.models import Image, ImageComment, Like


# Create your views here.
class Start(View):
    def get_images(self, model, order, count=7):
        return model.objects.order_by(order)[:count]


    def get(self, request):
        # images = Image.objects.order_by('-created')[:10]
        last_images = self.get_images(Image, '-created')
        top_of_the_top = self.get_images(Image, '-like')
        return render(request, 'start.html',
                      {'last_images': [last_images, 'last added'],
                       'top_of_the_top': [top_of_the_top, 'top of the top']})



class LastGenreImagesView(View):

    def get(self, request):
        images = Image.objects.order_by('genre')

class ImageView(View):

    def get(self, request, slug):
        back_button = request.META.get('HTTP_REFERER')
        image = Image.objects.get(slug=slug)
        access = {'like': True}
        try:
            user = User.objects.get(username=request.user)
            if Like.objects.filter(image=image, username=user):
                access = {'dislike': True}
        except:
            pass
        comments = ImageComment.objects.filter(image=image).order_by('-created')
        form_comments = ImageCommentForm()
        ctx = {'image': image, 'referer': back_button,
               'comments': comments,'form': form_comments,
               }
        ctx.update(access)
        return render(request, 'open_image.html',context=ctx)

    def post(self, request, slug):
        user = User.objects.get(username=request.user)
        image = Image.objects.get(pk=request.POST.get('image_id'))
        if request.POST.get('like'):
            Like.objects.create(image=image, username=user)
            image.increment_like()
            return redirect('image', slug=slug)
        if request.POST.get('dislike'):
            dislike = Like.objects.get(image=image, username=user)
            dislike.delete()
            image.decrease_like()
            return redirect('image', slug=slug)
        form_comment = ImageCommentForm(request.POST)
        if form_comment.is_valid():
            post = form_comment.save(commit=False)
            post.image = image
            post.user = user
            post.save()
            return redirect('image', slug=slug)
        return redirect('start')
