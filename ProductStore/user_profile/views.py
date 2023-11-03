from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.views.generic import CreateView, TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from . import models
from . import forms
from products.models import Product


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


class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            prod = []
            try:
                user_session = request.session
                products = user_session['products']

                for item in user_session['products']:
                    try:
                        prod.append(Product.objects.get(title=item['title']))
                    except:
                        pass
                print(prod)
            except:
                products = []

            return render(request, 'user_profile/profile.html', {'products': products, 'products_objects': prod})
        else:
            return redirect('login')


class AddProductToSessionView(View):
    def get(self, request, product_slug):
        try:
            product = Product.objects.get(slug=product_slug)

            # Словарь с информацией о товаре
            product_info = {
                'title': product.title,
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
                    if product_info['title'] not in str(user_session['products']):
                        user_session['products'].append(product_info)
                else:
                    # Если не существует, создаем новый список с товаром
                    user_session['products'] = [product_info]

                user_session.save()
        except:
            pass
        return redirect('main_page')


class ClearBasketView(View):
    def get(self, request):
        user_session = request.session
        # корзина представляет из себя список товаров, поэтому она всегда должна иметь тип list
        user_session['products'] = []
        return redirect('profile')


class DeleteProductIntoBasket(View):
    def get(self, request, product_title):
        try:
            user_session = request.session
            product = Product.objects.get(title=product_title)
            index = 0

            # ищем продукт в списке
            for item in user_session['products']:
                # нашли название продукта в сессии
                if item['title'] == product.title:
                    # удаляем этот продукт из сессии
                    user_session['products'].pop(index)
                    user_session.save()
                    break
                index += 1
        except:
            return redirect('profile')


# уменьшает кол-во продуктов в сессии юзера если operation = "-", иначе увеличивает
class ChangeCount(View):
    def get(self, request, product_title, operation):
        try:
            user_session = request.session
            product = Product.objects.get(title=product_title)
            index = 0

            # ищем продукт в списке
            for item in user_session['products']:
                # нашли название продукта в сессии
                if item['title'] == product.title:
                    # изменяем кол-во продуктов в корзине

                    if operation == '+':
                        user_session['products'][index]['count'] += 1
                    else:
                        user_session['products'][index]['count'] -= 1

                        # если товаров в корзине стало меньше 1, то удаляем этот товар из корзины
                        if user_session['products'][index]['count'] < 1:
                            user_session['products'].pop(index)

                    user_session.save()
                    break
                index += 1
        except:
            pass
        return redirect('profile')


