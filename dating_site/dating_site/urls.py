from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

djoser_router = DefaultRouter()
djoser_router.register("clients/create", UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf-auth/', include('rest_framework.urls')),
    path('api/', include(djoser_router.urls)),
    re_path(r'^api/', include('djoser.urls.authtoken')),
    path('', include('app_dating_site.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
