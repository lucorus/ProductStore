from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from . import models, forms, serializers, paginators
from apps.basket.models import Basket
from apps.products.utils import get_products_by_filter
from apps.products.models import Product
import logging

logger = logging.getLogger('main')


class ProfileView(LoginRequiredMixin, ListAPIView):
    serializer_class = ""
    pagination_class = ""

    def get_queryset(self):
        try:
            sorting = self.request.GET.get('sorting') or '-id'
            if sorting[0] == '-':
                reverse = '-'
                sorting = sorting.replace('-', '')
            else:
                reverse = ''
            products = get_products_by_filter(self.request)
            basket = Basket.objects.filter(owner=self.request.user, product__in=products).order_by(reverse + 'product__' + sorting).select_related('owner', 'product')
            return basket
        except Exception as ex:
            logger.error(ex)
            return []


class RegistrationView(APIView):
    def post(self, request):
        try:
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
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                return JsonResponse({'status': 'success'})
        except Exception as ex:
            logger.error(ex)
            return JsonResponse({'status': 'error'})

    def get(self, request):
        return render(request, 'users/register.html')


class LoginView(APIView):
    def post(self, request):
        try:
            user = models.CustomUser.objects.get(Q(email=request.POST['username']) | Q(username=request.POST['username']))
            if user and user.check_password(request.POST['password']):
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'incorrect password'})
        except Exception as ex:
            logger.error(ex)
            return JsonResponse({'status': 'error'})
        finally:
            return redirect('products:main_page')


@login_required
def user_logout(request):
    logout(request)
    return redirect('products:main_page')


class AddProductToFavorites(LoginRequiredMixin, APIView):
    def get(self, request):
        try:
            slug = request.GET.get('product_slug') or None
            if not slug:
                raise Exception('Not found slug')
            product = Product.objects.get(slug=slug)
            # если товар уже в избранном, то удаляем его
            if request.user.favorites.filter(slug=slug).exists():
                request.user.favorites.remove(product)
            else:
                request.user.favorites.add(product)
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'error', 'message': 'product not found'})


class CreateComment(LoginRequiredMixin, APIView):
    def post(self, request, product_slug):
        try:
            product = Product.objects.get(slug=product_slug)
            text = request.POST.get('text') or None
            estimation = request.POST.get('estimation') or None
            question = request.POST.get('comment_id') or None

            if question:
                # если написанный комментарий - ответ на другой комментарий (вопрос)
                question = models.Comment.objects.get(pk=question)
                question.answers.add(
                    models.Comment.objects.create(author=request.user, product=product, text=text, estimation=0)
                )
                question.save()
            else:
                models.Comment.objects.create(author=request.user, product=product, text=text, estimation=estimation)
            return JsonResponse({'status': 'success'})
        except Exception as ex:
            logger.error(ex)
            return JsonResponse({'status': 'error'})


class GetComments(ListAPIView):
    lookup_field = 'product_slug'
    serializer_class = serializers.CommentSerializer
    pagination_class = paginators.CommentPaginator

    def get_queryset(self):
        return models.Comment.objects.select_related('author', 'product')\
            .filter(product__slug=self.kwargs['product_slug']).filter(comment=None)


class GetAnswers(ListAPIView):
    lookup_field = 'comment_id'
    serializer_class = serializers.CommentSerializer
    pagination_class = paginators.CommentPaginator

    def get_queryset(self):
        return models.Comment.objects.showing_comments().select_related('author', 'product').filter(comment__pk=self.kwargs['comment_id'])


class CreateComplain(LoginRequiredMixin, APIView):
    def get(self, request):
        try:
            comment_id = request.GET.get('comment_id') or None
            comment = models.Comment.objects.get(id=comment_id)
            models.Complaints.objects.get_or_create(author=request.user, comment=comment)
            return JsonResponse({'status': 'success'})
        except Exception as ex:
            logger.error(ex)
            return JsonResponse({'status': 'error'})


