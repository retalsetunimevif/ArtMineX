from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from ArtMineX.forms import ImageCommentForm, GroupForm
from ArtMineX.models import Image, ImageComment, Like, Group


def get_images(model, order, count=7):
    return model.objects.order_by(order)[:count]


# Create your views here.
class Start(View):

    def get(self, request):
        # images = Image.objects.order_by('-created')[:10]
        last_images = get_images(Image, '-created')
        top_of_the_top = get_images(Image, '-like')
        return render(request, 'start.html',
                      {'last_images': [last_images, 'last added'],
                       'top_of_the_top': [top_of_the_top, 'top of the top']})


class LastGenreImagesView(View):

    def get(self, request):
        images = Image.objects.order_by('genre')


class ImageView(View):

    def get(self, request, slug):
        image = Image.objects.get(slug=slug)
        access = {'like': True}
        try:
            user = User.objects.get(username=request.user)
            if Like.objects.filter(image=image, username=user):
                access = {'dislike': True}
        except User.DoesNotExist:
            pass
        comments = ImageComment.objects.filter(image=image).order_by('-created')
        form_comments = ImageCommentForm()
        ctx = {'image': image, 'comments': comments,'form': form_comments,}
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


class GalleryView(View):
    def get(self, request):
        all_images = Image.objects.order_by('-created')
        return render(request, 'gallery.html', {'all_images': [all_images, 'All images']})


class GroupsFormView(View):
    def get(self, request):
        #form for createing group only for logged users
        form_group = GroupForm()
        groups = Group.objects.all()
        return render(request, 'groups.html',
                      {'groups': groups,
                       'form': form_group})

    def post(self, request):

        form_group = GroupForm(request.POST)
        if form_group.is_valid():
            group = form_group.save(commit=False)
            admin = request.user
            group.admin = admin
            group.save()
        return redirect('groups')


class GroupView(View):

    def get(self, request, group_name):
        group = Group.objects.get(name=group_name)
        members = group.members.all()
        pending_users = group.pending_users.all()
        last_images = group.image.order_by('-created')[:6]
        top_3_images = group.image.order_by('-like')[:3]
        return render(request, 'group.html', {
            'group': group,
            'members': members,
            'pending_users': pending_users,
            'last_images': [last_images, 'last added'],
            'top_3_images': [top_3_images, 'Top']
        })

    def post(self, request, group_name):
        group = Group.objects.get(name=group_name)
        members = group.members.all()
        pending_users = group.pending_users.all()
        if 'accept' in request.POST:
            pending_user = User.objects.get(pk=request.POST.get('pending_user'))
            group.accept_pending_user(user=pending_user)
        if 'reject' in request.POST:
            pending_user = User.objects.get(pk=request.POST.get('pending_user'))
            group.reject_pending_user(user=pending_user)
        if 'join' in request.POST:
            user_want_join = User.objects.get(pk=request.user.id)
            group.pending_users.add(user_want_join)
        return redirect('group', group_name=group_name)
