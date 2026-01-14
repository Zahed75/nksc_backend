from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('categories/', views.get_all_categories),
    path('all/', views.get_all_news),
    path('detail/<slug:slug>/', views.get_news_detail),
    path('urgent/', views.get_urgent_news),
    path('upcoming-events/', views.get_upcoming_events),
    path('research/', views.get_research_news),
    path('stats/', views.get_news_stats),
    
    # Admin endpoints
    path('admin/categories/create/', views.create_category),
    path('admin/create/', views.create_news),
    path('admin/update/<int:id>/', views.update_news),
    path('admin/delete/<int:id>/', views.delete_news),
    path('admin/all/', views.get_all_news_admin),
]