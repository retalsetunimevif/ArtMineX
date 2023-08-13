from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView

from Accounts.forms import UpdateUserAccountForm


class UpdateUserAccountFormView(UpdateView):
    model = User
    form_class = UpdateUserAccountForm
    template_name = 'forms.html'
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user})
