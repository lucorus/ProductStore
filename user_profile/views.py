from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.contrib.auth import login, logout
from django.views.generic import DetailView, ListView, CreateView
from . import models
from . import forms
from products.models import Product
from django.shortcuts import render, redirect
from django.http import JsonResponse


class RegistrationView(View):
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
            # Создание нового пользователя
            user = models.CustomUser.objects.create_user(username=username, password=password,
                                                         email=email, slug=slugify(username))
            user.save()
            login(request, user)

            return JsonResponse({'status': 'success'})

    def get(self, request):
        return render(request, 'user_profile/register.html')


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


@login_required
def user_logout(request):
    logout(request)
    return redirect('main_page')


class ProfileView(LoginRequiredMixin, ListView):
    login_url = 'main_page'
    redirect_field_name = 'main_page'
    template_name = 'user_profile/profile.html'
    context_object_name = 'user'

    def get_queryset(self):
        product_dict = {}
        try:
            user_session = self.request.session
            products = user_session['products']

            po = Product.objects.filter(Q(title__in=products)).distinct()
            # создаём словарь {название продукта: его данные}
            for i in range(len(user_session['products'])):
                product_dict[po[i].title] = po[i]
        except:
            products = {}
        return {'products': products, 'product_objects': product_dict}


class AddProductToSessionView(LoginRequiredMixin, View):
    login_url = 'main_page'
    redirect_field_name = 'main_page'

    def get(self, request):
        try:
            product = Product.objects.get(slug=request.GET.get('product_slug'))
            # Словарь с информацией о товаре
            product_info = {
                'price': product.price,
                'count': 1,
            }

            # Проверяем, авторизован ли пользователь
            if request.user.is_authenticated:
                # Получаем сессию пользователя
                user_session = request.session
                # Проверяем, существует ли ключ 'products' в сессии
                if 'products' in user_session:
                    # Если ключ существует, а в сессии (корзине) ещё нет такого продукта, то добавляем его
                    if product.title not in str(user_session['products']):
                        user_session['products'][product.title] = product_info

                else:
                    # Если не существует, создаем новый словарь с товаром
                    user_session['products'] = {}
                    user_session['products'][product.title] = product_info
                user_session.save()

            return JsonResponse({'success': True})
        except Exception as ex:
            print(ex)
            return JsonResponse({'success': False})


# очищает корзину
class ClearBasketView(LoginRequiredMixin, View):
    login_url = 'main_page'
    redirect_field_name = 'main_page'

    def get(self, request):
        try:
            user_session = request.session
            # корзина является список товаров, поэтому она всегда должна иметь тип dict
            user_session['products'] = {}
            request.session.save()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})


# удаляет определённый продукт из корзины
class DeleteProductIntoBasket(LoginRequiredMixin, View):
    login_url = 'main_page'
    redirect_field_name = 'main_page'

    def get(self, request):
        try:
            user_session = request.session
            product = Product.objects.get(slug=request.GET.get('product_slug'))

            user_session['products'].pop(product.title)
            user_session.save()

            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})


# уменьшает кол-во продуктов в сессии юзера если operation = "-", иначе увеличивает
class ChangeCount(LoginRequiredMixin, View):
    login_url = 'main_page'
    redirect_field_name = 'main_page'

    def get(self, request):
        try:
            user_session = request.session
            product = Product.objects.get(slug=request.GET.get('product_slug'))
            operation = request.GET.get('operation')

            if operation == '+':
                user_session['products'][product.title]['count'] += 1
            else:
                user_session['products'][product.title]['count'] -= 1
                # если кол-во продуктов в корзине с ключом product.title < 1, то удаляем его
                if user_session['products'][product.title]['count'] < 1:
                    user_session['products'].pop(product.title)
            user_session.save()

        except:
            pass
        return redirect('profile')


class AddToProductToFavorites(LoginRequiredMixin, View):
    def get(self, request):
        try:
            product_id = request.GET.get('product_id')
            if not product_id:
                raise Exception('product_id не найден')

            product = Product.objects.get(id=int(product_id))
            if product:
                if request.user.favourites.filter(id=product.id).exists():
                    request.user.favourites.remove(product)
                else:
                    request.user.favourites.add(product)
                request.user.save()
                return JsonResponse({'success': True})
            else:
                raise Exception('Продукт не найден')
        except Exception as ex:
            print(ex)
            return JsonResponse({'success': False})


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = models.Comments
    fields = ['text', 'estimation']
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        product_slug = self.request.POST.get('product_slug')
        form.instance.author = self.request.user
        form.instance.product = Product.objects.get(slug=product_slug)
        return super().form_valid(form)
