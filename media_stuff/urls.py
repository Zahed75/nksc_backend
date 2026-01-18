from django.urls import path
from . import views

urlpatterns = [
    # Main endpoints
    path('all/', views.get_all_gallery_events, name='all-gallery-events'),
    path('featured/', views.get_featured_gallery_events, name='featured-gallery-events'),
    path('latest/', views.get_latest_gallery_events, name='latest-gallery-events'),
    path('stats/', views.get_gallery_stats, name='gallery-stats'),
    path('search/', views.search_gallery_events, name='search-gallery-events'),
    
    # Event by slug
    path('event/<slug:slug>/', views.get_gallery_event_by_slug, name='gallery-event-detail'),
    path('event/<slug:slug>/images/', views.get_gallery_event_images, name='gallery-event-images'),
    
    # Categories
    path('categories/', views.get_all_categories, name='gallery-categories'),
    path('category/<slug:category_slug>/', views.get_gallery_by_category, name='gallery-by-category'),
    
    # Utilities
    path('years/', views.get_gallery_years, name='gallery-years'),
]