from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from rest_framework.views import APIView
from . import models, forms
from basket.models import Basket


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'users/profile.html'
    paginate_by = 1
    context_object_name = 'user'

    def get_queryset(self):
        return Basket.objects.filter(owner=self.request.user)


class LoginView(APIView):
    def post(self, request):
        try:
            user = models.CustomUser.objects.get(Q(email=request.POST['username']) | Q(username=request.POST['username']))
            if user and user.check_password(request.POST['password']):
                login(request, user)
        except Exception as ex:
            print(ex)
        finally:
            return redirect('products:main_page')


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
        return render(request, 'users/register.html')


class UserLoginView(APIView):
    def post(self, request):
        try:
            user = models.CustomUser.objects.get(Q(email=request.POST['username']) | Q(username=request.POST['username']))
            if user and user.check_password(request.POST['password']):
                login(request, user)
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'incorrect password'})
        except Exception as ex:
            print(ex)
            return JsonResponse({'status': 'error'})
        finally:
            return redirect('products:main_page')


@login_required
def user_logout(request):
    logout(request)
    return redirect('products:main_page')
