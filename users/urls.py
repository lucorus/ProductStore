from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.user_logout, name='logout'),
    path('registration', views.RegistrationView.as_view(), name='register'),
    path('add_to_favorites', views.AddProductToFavorites.as_view(), name='add_to_favorites'),
]


urlpatterns += staticfiles_urlpatterns()
