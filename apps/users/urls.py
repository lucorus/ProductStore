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
    path('create_comment/<slug:product_slug>', views.CreateComment.as_view(), name='create_comment'),
    path('get_comments/<slug:product_slug>', views.GetComments.as_view(), name='get_comments'),
    path('get_answers/<int:comment_id>', views.GetAnswers.as_view(), name='get_answers'),
    path('create_complaint', views.CreateComplain.as_view(), name='create_complaint'),
]


urlpatterns += staticfiles_urlpatterns()
