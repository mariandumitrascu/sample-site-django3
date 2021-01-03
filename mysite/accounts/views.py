from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView


from .forms import SignupForm


def signup(request):
    # return HttpResponse('hello from accounts application')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return HttpResponseRedirect(reverse('boards:home2'))
    else:
        form = SignupForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/signup.html', context)


    # refactored
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'accounts/my_account.html'
    # success_url = reverse_lazy('accounts:myaccount')
    success_url = reverse_lazy('boards:home2')

    def get_object(self):
        return self.request.user