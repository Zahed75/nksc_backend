from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # API Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema")),

    # APIs
    path("api/joujournals/", include("journal.urls")),
    path("api/publications", include("publications.urls")),
    path("api/media-staff", include("media_stuff.urls")),
    path("api/user-management", include("user_management.urls")),
]
