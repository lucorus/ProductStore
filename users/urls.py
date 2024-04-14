from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('logout', views.user_logout, name='logout'),
    path('registration', views.RegistrationView.as_view(), name='register'),
    # path('cart_change/', views.cart_change, name='cart_change'),
    # path('cart_remove/', views.cart_remove, name='cart_remove'),
]


urlpatterns += staticfiles_urlpatterns()
