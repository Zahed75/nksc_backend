from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images import urls as wagtailimages_urls
from wagtail import urls as wagtail_urls

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    path('cms/', include(wagtailadmin_urls)),  # Changed to avoid conflict with Django admin
    path('documents/', include(wagtaildocs_urls)),
    path('images/', include(wagtailimages_urls)),

    path('admin/', admin.site.urls),  # Django admin
    path('cms/', include(wagtailadmin_urls)),

    path("", include(wagtail_urls)),  # Wagtail frontend pages

    # Your app APIs
    path('api/journal/', include('journal.urls')),
    path('api/elibrary/', include('elibrary.urls')),
    path('api/media/', include('media_stuff.urls')),
    path('api/publications/', include('publications.urls')),
    path('api/users/', include('user_management.urls')),
]
