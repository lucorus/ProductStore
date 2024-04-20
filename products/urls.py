from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('categories', views.categories, name='categories'),
    path('products', views.Products.as_view(), name='products'),
    path('get_categories', views.CategoriesAPI.as_view(), name='get_categories'),
    path('product/<slug:slug>', views.DetailProductInfo.as_view(), name='product_detail'),
]


urlpatterns += staticfiles_urlpatterns()
