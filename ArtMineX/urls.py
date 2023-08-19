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
from django.urls import path, include
from ArtMineX import views
from ArtMineX import forms_view



urlpatterns = [
    path('', views.Start.as_view(), name='start'),
    path('add-image/', forms_view.AddImageFormView.as_view(), name='add-image'),
    path('add-genre/', forms_view.AddGenreFormView.as_view(), name='add-genre'),
    path('image/<slug:slug>/', views.ImageView.as_view(), name='image'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('groups/', views.GroupsFormView.as_view(), name='groups'),
    path('group/<group_name>/', views.GroupView.as_view(), name='group'),
]
