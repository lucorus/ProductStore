from django.urls import path

from api.views import Profile, FavoriteProducts, CommentViews, ComplainView


urlpatterns = [
    path("profile", Profile.as_view(), name="profile"),
    path("favorite", FavoriteProducts.as_view(), name="favorite"),
    path("comments", CommentViews.as_view(), name="comments"),
    path("complaints", ComplainView.as_view(), name="complaints")
]
