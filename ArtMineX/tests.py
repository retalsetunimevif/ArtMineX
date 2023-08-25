from random import randint

import pytest

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from Accounts.forms import UpdateUserAccountForm
from ArtMineX.forms import GroupForm
from ArtMineX.models import Image, Genre, Group, Like
from ArtMineX.pillow_tst import make_picture


# Create your tests here.

client = Client()


@pytest.mark.django_db
def test_start_index():
    """--- --- Test for view 'start' --- ---
    Test whether the start page displays properly for a non-logged-in user.
    Checks if login and registration links are present."""

    url = reverse('start')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Zaloguj' in str(response.content)
    assert 'Zarejestruj' in str(response.content)


@pytest.mark.django_db
def test_start_logged_user(user):
    """--- --- Test for view 'start' (logged user) --- ---
    Test whether the start page displays properly for a logged-in user.
    Checks if the username, 'add image', and 'Logout' links are present."""

    url = reverse('start')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert user.username in str(response.content)
    assert 'add image' in str(response.content)
    assert 'Logout' in str(response.content)


@pytest.mark.django_db
def test_login_not_exist():
    """--- --- Test for view 'login' (non-existent account) --- ---
    Test login with non-existent account.
    Checks if login with non-existing credentials
    redirects to the login page."""

    url = reverse('login')
    data = {'username': 'test1', 'password': 'test1'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.request['PATH_INFO'] == str(url)


@pytest.mark.django_db
def test_login(user):
    """--- --- Test for view 'login' (existing account) --- ---
    Test login with existing account.
    Checks if login with valid credentials redirects to the start page."""

    url = reverse('login')
    data = {'username': 'test1', 'password': 'test1'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('start'))


@pytest.mark.django_db
def test_add_image_user_not_logged():
    """--- --- Test for view 'add-image' (non-logged user) --- ---
    Test adding an image by a non-logged user.
    Checks if attempting to access the add-image page
    without logging in redirects to the login page."""

    url = reverse('add-image')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
    response = client.post(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_image_logged_user(user, genre):
    """--- --- Test for view 'add-image' (logged user) --- ---
    Test adding an image by a logged-in user with correct data.
    Checks if a logged-in user can successfully add an image
    with valid data."""

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


@pytest.mark.django_db
def test_for_logout(user):
    """--- --- Test for view 'logout' --- ---
    Test user logout.
    Checks if a logged-in user can successfully log out."""

    url = reverse('logout')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 302
    assert response['location'] == reverse('start')


@pytest.mark.django_db
def test_create_account_open_page(user):
    """--- --- Test for view 'add-user' (logged user) --- ---
    Test adding a user by an already logged-in user.
    Checks if a logged-in user is redirected
    when attempting to access the add-user page."""

    url = reverse('add-user')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 302
    assert response['Location'] == reverse('start')


@pytest.mark.django_db
def test_create_account():
    """--- --- Test for view 'add-user' (create account) --- ---
    Test creating a new account by a non-logged-in user.
    Checks if a non-logged-in user can enter on a page add-user."""

    url = reverse('add-user')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_account_with_correct_data():
    """--- --- Test for view 'add-user' (create account) --- ---
    Test creating a new account by a non-logged-in user.
    Checks if a non-logged-in user can create a new account
    with correct data."""

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


@pytest.mark.django_db
def test_create_account_with_existing_username(user):
    """--- --- Test for view 'add-user' (existing username) --- ---
    Test creating a new account with an existing username.
    Checks if creating an account with an already taken username
    returns an error message."""

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
    """--- --- Test for view 'add-user' (wrong email) --- ---
    Test creating a new account with invalid email addresses.
    Checks if creating an account with invalid email addresses
    returns appropriate error messages."""

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
    """--- --- Test for view 'add-user' (password mismatch) --- ---
    Test creating a new account with mismatched passwords.
    Checks if creating an account with mismatched passwords
    results in an error."""

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


@pytest.mark.django_db
def test_page_profile(user):
    """--- --- Test for view 'profile' (visitor) --- ---
    Test viewing a user profile as a visitor.
    Checks if a visitor can see a user's profile page."""

    url = reverse('profile', kwargs={'username': user})
    response = client.get(url)
    assert response.status_code == 200
    assert 'Edit' not in str(response.content)


@pytest.mark.django_db
def test_page_profile_with_owner(user):
    """--- --- Test for view 'profile' (owner) --- ---
    Test viewing own profile as the profile owner.
    Checks if a logged-in user can see their own profile page."""

    url = reverse('profile', kwargs={'username': user})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert 'Edit' in str(response.content)


@pytest.mark.django_db
def test_page_profile_for_not_existing_account():
    """--- --- Test for view 'profile' (not existing account) --- ---
    Test viewing a not existing account's profile.
    Checks if accessing a non-existing account's profile page
    results in a redirection."""

    url = reverse('profile', kwargs={'username': 'test1'})
    response = client.get(url)
    assert response.status_code == 302
    assert response['Location'] == reverse('404')


# --- --- Test for view 'update-profile' --- ---
# path('edit/', form_views.UpdateUserAccountFormView.as_view(), name='update-profile'),
@pytest.mark.django_db
def test_update_profile():
    """--- --- Test for view 'update-profile' (non-logged user) --- ---
    Test updating profile information by a non-logged user.
    Checks if attempting to access the update-profile page
    without logging in redirects to the login page."""

    response = client.get(reverse('update-profile'))
    assert response.status_code == 302
    assert response['Location'].startswith(reverse('login'))
    assert response['Location'].endswith(reverse('update-profile'))


@pytest.mark.django_db
def test_update_profile():
    """ --- --- Test for view 'update-profile' (logged user) --- ---
    Test updating profile information by a logged-in user.
    Checks if a logged-in user can successfully update
    their profile information."""

    user = User.objects.create(username='test1', email='test1@test1', first_name='te', last_name='st')
    user.set_password('test1')
    user.save()
    url = reverse('update-profile')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], UpdateUserAccountForm)
    data = {'last_name': 'last test',
            'first_name': 'first test',
            'email': 'email@test.pl'}
    response = client.post(url, data)
    assert response.status_code == 302
    updated_user = User.objects.get(pk=user.id)
    assert updated_user.last_name == 'last test'
    assert updated_user.first_name == 'first test'
    assert updated_user.email == 'email@test.pl'


@pytest.mark.django_db
def test_update_profile_wrong_email(user):
    """--- --- Test for view 'update-profile' (wrong email) --- ---
    Test updating profile with wrong email format.
    Checks if updating profile with an invalid email
    format returns an error."""

    url = reverse('update-profile')
    client.force_login(user)
    data = {'last_name': 'last test',
            'first_name': 'first test',
            'email': 'email@pl'}
    data2 = {'last_name': 'last test',
             'first_name': 'first test',
             'email': 'email.pl'}
    response1 = client.post(url, data)
    assert response1.status_code == 200
    assert User.objects.get(pk=user.id).email != data['email']
    response2 = client.post(url, data2)
    assert response2.status_code == 200
    assert User.objects.get(pk=user.id).email != data['email']


@pytest.mark.django_db
def test_image_open_page(images, users):
    """--- --- Test for view 'image' (visitor) --- ---
    Test viewing an image page as a visitor.
    Checks if a visitor can see an image page and the comment form."""

    image = images[randint(0, 9)]
    url = reverse('image', kwargs={'slug': image.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['user'] not in users  # ???
    assert 'To add a comment, <a href="' in str(response.content)


@pytest.mark.django_db
def test_image_open_page_with_logged_user(images, users, user):
    """--- --- Test for view 'image' (logged user) --- ---
    Test viewing an image page as a logged-in user.
    Checks if a logged-in user can see the image page,
    add a comment, and view their own comments."""

    image = images[randint(0, 9)]
    url = reverse('image', kwargs={'slug': image.slug})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert user.username == response.context['user'].username
    assert 'To add a comment, <a href="' not in str(response.content)
    assert len(response.context['comments']) == 0
    data = {'text': 'jakiś tam teks', 'image_id': image.id}
    response_post = client.post(url, data)
    assert response_post.status_code == 302
    response = client.get(url)
    assert len(response.context['comments']) == 1
    assert response.context['comments'][0].text == data['text']
    assert response.context['comments'][0].user == user


@pytest.mark.django_db
def test_image_open_page_like_image(images, users, user):
    """--- --- Test for view 'image' (like image) --- ---
    Test liking an image as a logged-in user.
    Checks if a logged-in user can like an image
    and updates the like count accordingly."""

    image = images[randint(0, 9)]
    likes = image.like
    url = reverse('image', kwargs={'slug': image.slug})
    client.force_login(user)
    response = client.get(url)
    assert likes == 0
    assert response.status_code == 200
    assert user.username == response.context['user'].username
    assert f'Likes {likes} people' in str(response.content)
    assert '<input name="like"' in str(response.content)
    assert '<input name="dislike"' not in str(response.content)
    data = {'image_id': image.id, 'like': 'like'}
    response_post = client.post(url, data)
    assert response_post.status_code == 302
    response = client.get(url)
    assert f'Likes {likes + 1} people' in str(response.content)
    assert '<input name="like"' not in str(response.content)
    assert '<input name="dislike"' in str(response.content)
    assert Image.objects.get(pk=image.id).like == 1


@pytest.mark.django_db
def test_image_open_page_dislike_image(images, users, user):
    """--- --- Test for view 'image' (dislike image) --- ---
    Test disliking an image as a logged-in user.
    Checks if a logged-in user can dislike an image
    and updates the like count accordingly."""

    image = images[randint(0, 9)]
    Like.objects.create(image=image, username=user)
    image.increment_like()
    likes = image.like
    url = reverse('image', kwargs={'slug': image.slug})
    client.force_login(user)
    response = client.get(url)
    assert likes == 1
    assert response.status_code == 200
    assert user.username == response.context['user'].username
    assert f'Likes {likes} people' in str(response.content)
    assert '<input name="like"'not in str(response.content)
    assert '<input name="dislike"' in str(response.content)
    data = {'image_id': image.id, 'dislike': 'dislike'}
    response_post = client.post(url, data)
    assert response_post.status_code == 302
    response = client.get(url)
    assert f'Likes {likes - 1} people' in str(response.content)
    assert '<input name="like"' in str(response.content)
    assert '<input name="dislike"' not in str(response.content)
    assert Image.objects.get(pk=image.id).like == 0


@pytest.mark.django_db
def test_add_genre_not_logged():
    """--- --- Test for view 'add-genre' (not logged) --- ---
    Test adding a genre by a non-logged user.
    Checks if attempting to access the add-genre page without
    logging in redirects to the login page."""

    url = reverse('add-genre')
    response = client.get(url)
    assert response.status_code == 302
    assert response['Location'].startswith(reverse('login'))


@pytest.mark.django_db
def test_add_genre_logged(user, genre):
    """--- --- Test for view 'add-genre' (logged) --- ---
    Test adding a genre by a logged-in user.
    Checks if a logged-in user can successfully add a new genre."""

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


@pytest.mark.django_db
def test_gallery_view_empty_gallery():
    """--- --- Test for view 'gallery' (empty gallery) --- ---
    Test viewing the gallery with no images.
    Checks if the gallery displays properly when there are no images."""

    url = reverse('gallery')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['all_images'][0]) == 0


@pytest.mark.django_db
def test_gallery_view_with_gallery_list(images):
    """--- --- Test for view 'gallery' (with images) --- ---
    Test viewing the gallery with images.
    Checks if the gallery displays images when they are present."""

    url = reverse('gallery')
    response = client.get(url)
    assert len(response.context['all_images'][0]) == len(images)


@pytest.mark.django_db
def test_gallery_images_first_is_last(images):
    """--- --- Test for view 'gallery' (images order) --- ---
    Test the order of images in the gallery.
    Checks if the order of images in the gallery is as expected."""

    url = reverse('gallery')
    response = client.get(url)
    # first image of list is last added
    assert images[-1] == response.context['all_images'][0][0]
    # last image of list is first added
    count = len(response.context['all_images'][0])
    assert images[0] == response.context['all_images'][0][count-1]


@pytest.mark.django_db
def test_view_groups_no_logged_user(group):
    """--- --- Test for view 'groups' (not logged user) --- ---
    Test viewing groups page by a non-logged user.
    Checks if a non-logged user can view the groups page
    and no form is present."""

    url = reverse('groups')
    response = client.get(url)
    assert response.status_code == 200
    assert group.name in str(response.content)
    assert '<form' not in str(response.content)


@pytest.mark.django_db
def test_view_groups_logged_user(user, groups):
    """--- --- Test for view 'groups' (logged user) --- ---
    Test viewing groups page by a logged-in user.
    Checks if a logged-in user can view the groups page
    and the group form is present."""

    url = reverse('groups')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['groups']) == len(groups)
    assert isinstance(response.context['form'], GroupForm)
    response2 = client.post(url, {'name': 'Group number one'})
    assert response2.status_code == 302
    assert Group.objects.count() - len(groups) == 1
    response3 = client.get(url)
    assert 'Group number one' in str(response3.content)


@pytest.mark.django_db
def test_view_groups_add_existing_group(user, groups):
    """--- --- Test for view 'groups' (with existing group) --- ---
    Test adding an existing group in the 'groups' view
    Tests adding an existing group by a logged-in user,
    checks for existing group message and group count."""

    url = reverse('groups')
    client.force_login(user)
    response = client.post(url, {'name': 'group5'})
    assert response.status_code == 200
    assert 'Group with this Name already exists.' in str(response.content)
    assert Group.objects.count() == len(groups)


@pytest.mark.django_db
def test_group_view_user_no_member(user, groups):
    """--- --- Test for view 'group' (user not in group) --- ---
    Test a non-member user's interaction with a group.
    Checks if the user can join the group and waits for admin approval."""

    group = groups[0]
    url = reverse('group', kwargs={'group_name': group.name})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert user.username not in response.context['members']
    assert '<input type="submit" name="join"' in str(response.content)
    response_post = client.post(url, {'join': 'Join'})
    assert response_post.status_code == 302
    response = client.get(url)
    assert 'You have to wait for admin approval' in str(response.content)


@pytest.mark.django_db
def test_group_view_admin_with_no_pending_users(users, groups):
    """--- --- Test for view 'group' (admin with no pending users) --- ---
    Test an admin's view of a group with no pending users.
    Ensures that admin sees the correct message when no users are pending."""

    user = users[0]
    group = groups[0]
    assert group.admin == user
    client.force_login(user)
    response = client.get(reverse('group', kwargs={'group_name': group}))
    assert response.status_code == 200
    assert 'Users waiting in queue to be accepted 0' in str(response.content)


@pytest.mark.django_db
def test_group_view_admin_with_pending_users(user, group, users, pending_users):
    """--- --- Test for view 'group' (admin with pending users) --- ---
    Test an admin's view of a group with pending users.
    Checks if admin can see pending users and their associated actions."""

    assert group.admin == user
    client.force_login(user)
    response = client.get(reverse('group', kwargs={'group_name': group}))
    assert response.status_code == 200
    assert group.pending_users.count() == len(users)
    assert response.context['pending_users'] is not None
    assert len(response.context['pending_users']) == len(users)
    assert '<input type="submit" name="accept"' in str(response.content)
    assert '<input type="submit" name="reject"' in str(response.content)


@pytest.mark.django_db
def test_group_view_admin_with_pending_users_accept(user, group, users, pending_users):
    """--- --- Test for view 'group' (admin accepting pending user) --- ---
    Test an admin's acceptance of a pending user in a group.
    Validates if admin can accept a pending user and the member count increases."""

    assert group.admin == user
    members = group.members.count()
    client.force_login(user)
    url = reverse('group', kwargs={'group_name': group})
    response = client.get(url)
    assert response.status_code == 200
    assert 'Number of users: 1' in str(response.content)
    assert group.pending_users.count() == len(users)
    pending_user = users[1].id
    data = {'pending_user': pending_user, 'accept': 'Accept'}
    response_post = client.post(url, data)
    assert response_post.status_code == 302
    response = client.get(url)
    members2 = group.members.count()
    assert members2 - members == 1
    assert f'Number of users: {members + 1}' in str(response.content)
    assert pending_user not in response.context['pending_users']


@pytest.mark.django_db
def test_group_view_admin_with_pending_users_reject(user, group, users, pending_users):
    """--- --- Test for view 'group' (admin rejecting pending user) --- ---
    Test an admin's rejection of a pending user in a group.
    Confirms that admin can reject a pending user, removing them from the queue."""

    assert group.admin == user
    client.force_login(user)
    url = reverse('group', kwargs={'group_name': group})
    response = client.get(url)
    assert response.status_code == 200
    assert group.pending_users.count() == len(users)
    pending_user = users[1].id
    data = {'pending_user': pending_user, 'reject': 'Reject'}
    response_post = client.post(url, data)
    assert response_post.status_code == 302
    response = client.get(url)
    assert pending_user not in response.context['pending_users']
    assert pending_user not in response.context['members']
    assert len(users) - group.pending_users.count() == 1
