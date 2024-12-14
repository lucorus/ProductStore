from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('basket_add/<slug:product_slug>', views.AddBasket.as_view(), name='basket_add'),
    path('change_count/<slug:product_slug>/<str:operation>', views.ChangeCountProductInBasket.as_view(), name='change_count'),
    path('delete/<slug:product_slug>', views.DeleteBasket.as_view(), name='delete_basket'),
]


urlpatterns += staticfiles_urlpatterns()
