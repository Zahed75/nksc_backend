from django.urls import path
from .views import StaffAPIView, DepartmentAPIView, StaffStatsAPIView

urlpatterns = [
    # Main staff API (handles all operations)
    path('', StaffAPIView.as_view(), name='staff-api'),
    path('<int:id>/', StaffAPIView.as_view(), name='staff-detail'),
    
    # Departments
    path('departments/', DepartmentAPIView.as_view(), name='departments'),
    
    # Statistics
    path('stats/', StaffStatsAPIView.as_view(), name='staff-stats'),
]