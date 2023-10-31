from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('register', views.Register.as_view(), name='register'),
    path('logout', views.logout, name='logout'),
    path('login', views.UserLoginView.as_view(), name='login'),
]
