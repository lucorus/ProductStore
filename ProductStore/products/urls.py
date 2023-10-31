from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='main_page'),
    path('detail/<slug:slug>', views.ProductDetailView.as_view(), name='detail'),
    path('categories', views.CategoryView.as_view(), name='categories'),
]


urlpatterns += staticfiles_urlpatterns()
