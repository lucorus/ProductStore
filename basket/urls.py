from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('basket_add/', views.AddBasket.as_view(), name='basket_add'),
    # path('cart_change/', views.cart_change, name='cart_change'),
    # path('cart_remove/', views.cart_remove, name='cart_remove'),
]


urlpatterns += staticfiles_urlpatterns()
