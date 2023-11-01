from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('register', views.Register.as_view(), name='register'),
    path('logout', views.user_logout, name='logout'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('add_basket/<slug:product_slug>', views.AddProductToSessionView.as_view(), name='add_to_basket'),
    path('clear_basket/', views.ClearBasketView.as_view(), name='clear_basket'),
    path('delete_product_into_basket/<str:product_title>', views.DeleteProductIntoBasket.as_view(),
         name='delete_product_into_basket'),
    path('change_count/<str:product_title>/<str:operation>', views.ChangeCount.as_view(),
         name='change_count'),
]


urlpatterns += staticfiles_urlpatterns()
