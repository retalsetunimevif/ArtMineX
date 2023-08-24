import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from ArtMineX.models import Image, Genre
from ArtMineX.pillow_tst import make_picture


# Create your tests here.

client = Client()

# --- --- Test for view 'start' --- ---
# path('', views.Start.as_view(), name='start'),
@pytest.mark.django_db
def test_start_index():
    url = reverse('start')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Zaloguj' in str(response.content)
    assert 'Zarejestruj' in str(response.content)


@pytest.mark.django_db
def test_start_logged_user(user):
    url = reverse('start')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert user.username in str(response.content)
    assert 'add image' in str(response.content)
    assert 'Logout' in str(response.content)


# --- --- Test for view 'login' --- ---
# path('login/', views.LoginFormView.as_view(), name='login'),
@pytest.mark.django_db
def test_login_not_exist():
    """Test for login not existing account"""
    url = reverse('login')
    data = {'username': 'test1', 'password': 'test1'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.request['PATH_INFO'] == str(url)


@pytest.mark.django_db
def test_login(user):
    """Test for login existing account"""
    url = reverse('login')
    data = {'username': 'test1', 'password': 'test1'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('start'))


# --- --- Test for view 'add-image' --- ---
# path('add-image/', forms_view.AddImageFormView.as_view(), name='add-image'),
@pytest.mark.django_db
def test_add_image_user_not_logged():
    url = reverse('add-image')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
    response = client.post(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_image_logged_user(user, genre):
    url = f'/artminex/add-image/?next=/accounts/profile/{user.username}/'
    client.force_login(user)
    response_get = client.get(url,  follow=True)
    print(response_get.redirect_chain)
    assert response_get.status_code == 200
    picture = make_picture()
    data = {'title': 'abc', 'description': 'description',
            'genre': str(genre.id), 'image': picture}
    response_post = client.post(url, data)
    assert response_post.status_code == 302
    assert Image.objects.get(title=data['title'])
    assert response_post['Location'] == reverse('profile', kwargs={'username': user.username})


# --- --- Test for view 'logout' --- ---
# path('logout/', views.LogoutView.as_view(), name='logout'),
@pytest.mark.django_db
def test_for_logout(user):
    url = reverse('logout')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 302
    assert response['location'] == reverse('start')


# --- --- Test for view 'add-user' --- ---
# path('add-user/', views.AddUserFormView.as_view(), name='add-user'),
@pytest.mark.django_db
def test_create_account_open_page(user):
    """Test for user if allready logged"""
    url = reverse('add-user')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 302
    assert response['Location'] == reverse('start')

@pytest.mark.django_db
def test_create_account():
    """Test for creating new account, not logged user"""
    url = reverse('add-user')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_account_with_correct_data():
    """Test for creating new account, all data is correct"""
    url = reverse('add-user')
    users = User.objects.count()
    data = {'username': 'test1',
            'email': 'test1@test1.pl',
            'password1': 'test123',
            'password2': 'test123',
            }

    response = client.post(url, data)
    assert response.status_code == 302
    assert User.objects.count() - users == 1
    response = client.get(url)
    assert data['username'] in str(response.content)
    print(response.content)


@pytest.mark.django_db
def test_create_account_with_existing_username(user):
    """Test for create account with existing user"""
    url = reverse('add-user')
    data = {'username': 'test1',
            'email': 'test2@test2.pl',
            'password1': 'test123',
            'password2': 'test123',
            }
    response = client.post(url, data)
    assert response.status_code == 200
    user = User.objects.get(username=data['username'])
    assert user.email != data['email']
    assert 'A user with that username already exists.' in str(response.content)


@pytest.mark.django_db
def test_create_account_with_wrong_data_email(users):
    """Test for wrong email adress"""
    url = reverse('add-user')
    data = {'username': 'someone',
            'email': 'someone.pl',
            'password1': 'somepassword',
            'password2': 'somepassword',
            }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'email must contain &quot;@&quot; sign!' in str(response.content)
    assert User.objects.count() == len(users)
    data_2 = {'username': 'someone',
              'email': 'someone@someone',
              'password1': 'somepassword',
              'password2': 'somepassword',
              }
    response = client.post(url, data_2)
    assert response.status_code == 200
    assert 'Enter a valid email address' in str(response.content)
    assert User.objects.count() == len(users)


@pytest.mark.django_db
def test_create_account_with_wrong_data_password():
    """Test for password not the same password"""
    url = reverse('add-user')
    data = {'username': 'someone',
            'email': 'someone@someone.pl',
            'password1': 'somepassword',
            'password2': 'notsamepassword',
            }
    response = client.post(url)
    assert response.status_code == 200
    assert f'{data["username"]}'not in str(response.content)
    assert User.objects.count() == 0


# --- --- Test for view 'profile' --- ---
# path('profile/<username>/', views.UserProfileView.as_view(), name='profile'),
@pytest.mark.django_db
def test_page_profile(user):
    """Test for the visitor"""
    url = reverse('profile', kwargs={'username': user})
    response = client.get(url)
    assert response.status_code == 200
    assert 'Edit' not in str(response.content)


@pytest.mark.django_db
def test_page_profile_with_owner(user):
    """Test for owner visiting self profile"""
    url = reverse('profile', kwargs={'username': user})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert 'Edit' in str(response.content)


@pytest.mark.django_db
def test_page_profile_for_not_existing_account():
    """Test for visiting not existing account"""
    url = reverse('profile', kwargs={'username': 'test1'})
    response = client.get(url)
    assert response.status_code == 302
    assert response['Location'] == reverse('404')


# --- --- Test for view 'update-profile' --- ---
# path('edit/', form_views.UpdateUserAccountFormView.as_view(), name='update-profile'),


# --- --- Test for view 'image' --- ---
# path('image/<slug:slug>/', views.ImageView.as_view(), name='image'),


# --- --- Test for view 'add-genre' --- ---
# path('add-genre/', forms_view.AddGenreFormView.as_view(), name='add-genre'),
@pytest.mark.django_db
def test_add_genre_not_logged():
    url = reverse('add-genre')
    response = client.get(url)
    assert response.status_code == 302
    assert response['Location'].startswith(reverse('login'))


@pytest.mark.django_db
def test_add_genre_logged(user, genre):
    genres = Genre.objects.count()
    url = reverse('add-genre')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    data = {'genre': 'new genre test'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Genre.objects.count() - genres == 1
    assert response['Location'] == reverse('add-genre')


# --- --- Test for view 'gallery' --- ---
# path('gallery/', views.GalleryView.as_view(), name='gallery'),
@pytest.mark.django_db
def test_gallery_view_empty_gallery():
    url = reverse('gallery')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['all_images'][0]) == 0

@pytest.mark.django_db
def test_gallery_view_with_gallery_list(images):
    url = reverse('gallery')
    response = client.get(url)
    assert len(response.context['all_images'][0]) == len(images)


@pytest.mark.django_db
def test_gallery_images_first_is_last(images):
    url = reverse('gallery')
    response = client.get(url)
    # first is last added
    assert images[-1] == response.context['all_images'][0][0]
    # last is first added
    lenght = len(response.context['all_images'][0])
    assert images[0] == response.context['all_images'][0][lenght-1]




# --- --- Test for view 'groups' --- ---
# path('groups/', views.GroupsFormView.as_view(), name='groups'),


# --- --- Test for view 'group' --- ---
# path('group/<group_name>/', views.GroupView.as_view(), name='group'),
