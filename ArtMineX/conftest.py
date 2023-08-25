import pytest

from django.contrib.auth.models import User

from ArtMineX.models import Genre, Group, Image
from ArtMineX.pillow_tst import make_picture


@pytest.fixture
def user():
    """Fixture: Creates and returns a test user with specific details."""
    user = User.objects.create(username='test1',
                               email='test1@test1.pl',
                               first_name='te',
                               last_name='st')
    user.set_password('test1')
    user.save()
    return user


@pytest.fixture
def users():
    """Fixture: Creates and returns a test users list with specific details."""
    lst = []
    for x in range(1, 11):
        user = User.objects.create(username=f'test_{x}',
                                   email=f'email{x}@test{x}.com',
                                   first_name=f'te{x}',
                                   last_name=f'st{x}')
        lst.append(user)
    return lst


@pytest.fixture
def genre():
    """Fixture: Creates and returns a test genre with specific details."""
    return Genre.objects.create(genre='Genre test')


@pytest.fixture
def genres():
    """Fixture: Creates and returns a test genres list with specific details."""
    lst = []
    for x in range(10):
        g = Genre.objects.create(genre=f'Genre {x}')
        lst.append(g)
    return lst


@pytest.fixture
def group(user):
    """Fixture: Creates and returns a test group with specific details."""
    group = Group()
    group.name = 'Group test'
    group.admin = user
    group.save()
    return group


@pytest.fixture
def groups(users):
    """Fixture: Creates and returns a test groups list with specific details."""
    lst = []
    for x in range(1, 11):
        user = users[x-1]
        gs = Group(name=f'group{x}', admin=user)
        gs.save()
        lst.append(gs)
    return lst


@pytest.fixture
def images(users, genres):
    """Fixture: Creates and returns a test images list with specific details."""
    lst = []
    for x in range(1, 11):
        img = Image.objects.create(title=f'title_{x}',
                                   description=f'description_{x}',
                                   user=users[x-1],
                                   genre=genres[x-1],
                                   image=make_picture())
        lst.append(img)
    return lst


@pytest.fixture
def pending_users(group, users):
    """Fixture: Creates and associates test pending users with a specific group."""
    for pending_user in users:
        group.pending_users.add(pending_user)
