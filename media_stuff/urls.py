from django.urls import path
from . import views

urlpatterns = [
    # Main endpoints
    path('all/', views.get_all_gallery_events, name='all-gallery-events'),
    path('event/<slug:slug>/', views.get_gallery_event_by_slug, name='gallery-event-detail'),
    path('event/<slug:slug>/images/', views.get_gallery_event_images, name='gallery-event-images'),
    path('event/<slug:slug>/videos/', views.get_gallery_event_videos, name='gallery-event-videos'),

    # Categories
    path('categories/', views.get_all_categories, name='gallery-categories'),

    # Media types
    path('photos/', views.get_photo_galleries, name='photo-galleries'),
    path('videos/', views.get_video_galleries, name='video-galleries'),

    # Utilities
    path('years/', views.get_gallery_years, name='gallery-years'),
    path('stats/', views.get_gallery_stats, name='gallery-stats'),
    path('search/', views.search_gallery_events, name='search-gallery-events'),
]