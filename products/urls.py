from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='main_page'),
    path('detail/<slug:slug>', views.ProductDetailView.as_view(), name='detail'),
    path('categories', views.CategoryView.as_view(), name='categories'),
    path('category/<slug:slug>', views.ProductInCategoryView.as_view(), name='products_in_category'),
    # path('create_comment', views.CreateCommentView.as_view(), name='create_comment'),
]


urlpatterns += staticfiles_urlpatterns()
