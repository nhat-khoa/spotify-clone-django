"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Cấu hình Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Spotify Clone API",
        default_version="v1",
        description="API documentation for Spotify Clone",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.artists.urls')),
    path('api/', include('apps.tracks.urls')),
    path('api/', include('apps.podcasts.urls')),
    path('api/', include('apps.interactions.urls')),
    path('api/', include('apps.categories.urls')),
    path('api/', include('apps.subscriptions.urls')),
    path('api/', include('apps.albums.urls')),

    # path('', include('apps.group_sessions.urls')),
    # path('', include('apps.analytics.urls')),

    path("api/auth/", include("apps.authen.urls")),
    path('api/favorites/', include('apps.favorites.urls')),

    # Swagger
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]



if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 