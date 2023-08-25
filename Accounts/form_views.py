from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from Accounts.forms import UpdateUserAccountForm


# class UpdateUserAccountFormView(LoginRequiredMixin, UpdateView):
#     model = User
#     form_class = UpdateUserAccountForm
#     template_name = 'forms.html'
#     queryset = User.objects.all()
#
#     def get_object(self):
#         return self.request.user
#
#     def get_success_url(self):
#         return reverse_lazy('profile', kwargs={'username': self.request.user})


class UpdateUserAccountFormView(LoginRequiredMixin, UpdateView):
    def get(self, request):
        user = request.user
        form = UpdateUserAccountForm(instance=user)
        return render(request, 'forms.html', {'form': form})

    def post(self, request):
        user = User.objects.get(pk=request.user.id)
        form = UpdateUserAccountForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('profile', username=user.username)
        return render(request, 'forms.html', {'form': form})

