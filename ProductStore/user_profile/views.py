from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.generic import CreateView, TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from . import models
from . import forms


class Register(View):
    def get(self, request):
        return render(request, 'user_profile/register.html', {'form': forms.CustomUserCreationForm})

    def post(self, request):
        form = forms.CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.slug = slugify(str(user.username))
            user.save()
            login(request, user)
        return redirect('main_page')


def user_register(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.slug = str(user.username)
            user.save()
            login(request, user)
            return redirect('main_page')
    else:
        form = forms.CustomUserCreationForm()
    return render(request, 'user_profile/register.html', {'form': form})


class UserLoginView(View):
    def get(self, request):
        form = forms.UserLoginForm()
        return render(request, 'user_profile/login.html', {'form': form})

    def post(self, request):
        form = forms.UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')
        return redirect('login')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'user_profile/profile.html')
        else:
            return redirect('login')

