from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProfilView.as_view(), name='profile'),
    path('logout', views.user_logout, name='logout'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('add_basket', views.AddProductToSessionView.as_view(), name='add_to_basket'),
    path('clear_basket', views.ClearBasketView.as_view(), name='clear_basket'),
    path('delete_product_into_basket', views.DeleteProductIntoBasket.as_view(),
         name='delete_product_into_basket'),
    path('change_count', views.ChangeCount.as_view(), name='change_count'),
    path('registration', views.RegistrationView.as_view(), name='register'),
]


urlpatterns += staticfiles_urlpatterns()
