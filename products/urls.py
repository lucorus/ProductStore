from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('products', views.Products.as_view(), name='products'),
    path('', views.main_page, name='main_page'),
    path('categories', views.CategoriesView.as_view(), name='categories'),
    path('category/<slug:category_slug>', views.Products.as_view(), name='category_detail'),
    path('subcategory/<slug:subcategory_slug>', views.Products.as_view(), name='subcategory_detail'),
    path('product/<slug:slug>', views.DetailProductInfo.as_view(), name='product_detail'),
]


urlpatterns += staticfiles_urlpatterns()
