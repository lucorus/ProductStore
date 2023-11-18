from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic import ListView, DetailView, FormView, CreateView
from user_profile.forms import UserLoginForm
from . import models


class MainView(ListView, FormView):
    template_name = 'products/main_page.html'
    context_object_name = 'product'
    form_class = UserLoginForm
    paginate_by = 3

    def get_queryset(self):
        products = models.Product.objects.select_related('subcategory').all().defer(
            'subcategory__category__slug',
            'subcategory__category__image',
            'subcategory__image',
            'subcategory__slug').order_by('id')
        return products


# детальная информация о продукте
class ProductDetailView(DetailView, FormView):
    context_object_name = 'product'
    template_name = 'products/detail.html'
    form_class = UserLoginForm

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        try:
            return models.Product.objects.select_related('subcategory').get(slug=slug)
        except:
            raise Http404('Такого товара не существует')


# выводим все категории и подкатегории
class CategoryView(ListView, FormView):
    template_name = 'products/categories.html'
    context_object_name = 'categories'
    form_class = UserLoginForm
    paginate_by = 2
    queryset = models.Category.objects.all().order_by('id')


# возвращает продукты, находящиеся в категории/подкатегории с slug'ом = slug
class ProductInCategoryView(ListView, FormView):
    template_name = 'products/main_page.html'
    context_object_name = 'product'
    form_class = UserLoginForm
    paginate_by = 2

    def get_queryset(self):
        slug = self.kwargs['slug']
        queryset = models.Product.objects.select_related('subcategory').filter(
            Q(subcategory__slug=slug) | Q(subcategory__category__slug=slug)
        ).order_by('id')
        return queryset


# class CreateCommentView(CreateView, LoginRequiredMixin):
#     model = models.Comments
#     fields = ['text', 'estimation']
#     success_url = reverse_lazy('main_page')
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.product = models.Product.objects.get(slug=self.request.POST.get('product_slug'))
#         response = super().form_valid(form)
#         return JsonResponse({'comment_id': self.object.id})


# class CreateCommentView(View):
#     def post(self, request, *args, **kwargs):
#         product_slug = request.POST.get('product_slug')
#         text = request.POST.get('text')
#         estimation = request.POST.get('estimation')
#         author = request.user
#
#         # Создание комментария
#         models.Comments.objects.create(
#             text=text,
#             author=author,
#             product= models.Product.objects.get(slug=product_slug),
#             estimation=estimation
#         )
#
#         return JsonResponse({'code': 200})
#
#
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.edit import CreateView
# from .models import Comments, Product

class CreateCommentView(LoginRequiredMixin, CreateView):
    model = models.Comments
    fields = ['text', 'estimation']
    template_name = 'products/file.html'
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        product_slug = self.request.POST.get('product_slug')
        form.instance.author = self.request.user
        form.instance.product = models.Product.objects.get(slug=product_slug)
        return super().form_valid(form)
