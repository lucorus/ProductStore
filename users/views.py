from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView
from rest_framework.views import APIView

from . import models


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return models.CustomUser.objects.get(slug=self.request.user.slug)


class RegistrationView(APIView):
    def post(self, request):
        username = str(request.POST.get('username'))
        password = str(request.POST.get('password'))
        email = str(request.POST.get('email'))

        # Проверка данных формы
        errors = {}
        if models.CustomUser.objects.filter(username=username).exists():
            errors['username'] = 'Пользователь с таким именем уже существует!'
        if len(password) < 8:
            errors['password'] = 'Пароль должен состоять минимум из 8 символов'
        if models.CustomUser.objects.filter(email=email).exists():
            errors['email'] = 'Пользователь с такой почтой уже существует!'

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors})
        else:
            user = models.CustomUser.objects.create_user(username=username, password=password,
                                                         email=email)
            user.save()
            login(request, user)

            return JsonResponse({'status': 'success'})

    def get(self, request):
        return render(request, 'user_profile/register.html')


class UserLoginView(APIView):
    def post(self, request):
        try:
            user = models.CustomUser.objects.get(Q(email=request.POST['username']) | Q(username=request.POST['username']))
            if user and user.check_password(request.POST['password']):
                login(request, user)
        finally:
            return redirect('main_page')


@login_required
def user_logout(request):
    logout(request)
    return redirect('main_page')
