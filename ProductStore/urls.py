from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('v1/', include('api.urls')),

    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('', include('apps.products.urls', namespace='products')),
    path('user/', include('apps.users.urls', namespace='users')),
    path('basket/', include('apps.basket.urls', namespace='basket')),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # url(r'^auth/', include('djoser.urls.authtoken')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

