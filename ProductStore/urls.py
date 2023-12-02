from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('user/', include('user_profile.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA__ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA__ROOT)
