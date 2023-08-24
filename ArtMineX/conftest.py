import pytest

from django.contrib.auth.models import User

from ArtMineX.models import Genre, Group, Image
from ArtMineX.pillow_tst import make_picture


@pytest.fixture
def user():
    user = User.objects.create(username='test1', email='test1@test1', first_name='te', last_name='st')
    user.save()
    user.set_password('test1')
    user.save()
    return user

@pytest.fixture
def users():
    lst = []
    for x in range(1,11):
        user = User.objects.create(username=f'test_{x}', email=f'email{x}@test{x}.com', first_name=f'te{x}', last_name=f'st{x}')
        lst.append(user)
    return lst
@pytest.fixture
def genres():
    lst = []
    for x in range(10):
        g = Genre.objects.create(genre=f'Genre {x}')
        lst.append(g)
    return lst

@pytest.fixture
def genre():
    return Genre.objects.create(genre='Genre test')


@pytest.fixture
def group(user):
    return Group.objects.create(name='Group test', admin=user)

@pytest.fixture
def images(users, genres):
    lst = []
    for x in range(1,11):
        img = Image.objects.create(title=f'title_{x}', description=f'description_{x}', user=users[x-1],
            genre= genres[x-1], image=make_picture())
        lst.append(img)
    return lst

