from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api.views import (
    Profile, FavoriteProducts, CommentViews, ComplainView, CategoriesView, ProductViewSet, CustomUserViewSet,
    BasketViews
)


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),

    path("profile", Profile.as_view(), name="profile"),
    path("favorite", FavoriteProducts.as_view(), name="favorite"),
    path("comments", CommentViews.as_view(), name="comments"),
    path("complaints", ComplainView.as_view(), name="complaints"),

    path("categories", CategoriesView.as_view(), name="categories"),

    path("basket", BasketViews.as_view(), name="basket"),
]
