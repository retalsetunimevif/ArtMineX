"""
URL configuration for project_digfart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from Accounts import views
from Accounts import form_views



urlpatterns = [
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('add-user/', views.AddUserFormView.as_view(), name='add-user'),
    path('profile/<username>/', views.UserProfileView.as_view(), name='profile'),
    path('edit/', form_views.UpdateUserAccountFormView.as_view(), name='update-profile'),

]
