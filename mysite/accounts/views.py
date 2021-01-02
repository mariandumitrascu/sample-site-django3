from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

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