from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('categories', views.CategoriesView.as_view(), name='categories'),
    # path('cart_change/', views.cart_change, name='cart_change'),
    # path('cart_remove/', views.cart_remove, name='cart_remove'),
]


urlpatterns += staticfiles_urlpatterns()
