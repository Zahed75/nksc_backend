from django.urls import path
from .views import (
    AboutAPIView,
    AboutSectionsAPIView,
    TimelineEventsAPIView,
    DirectorsAPIView,
    CurrentDirectorAPIView,
    FacilitiesAPIView,
    StatisticsAPIView,
    ContactInfoAPIView
)

urlpatterns = [
    # Main endpoint - get all about data
    path('', AboutAPIView.as_view(), name='about-data'),
    
    # Individual endpoints
    path('sections/', AboutSectionsAPIView.as_view(), name='about-sections'),
    path('timeline/', TimelineEventsAPIView.as_view(), name='timeline-events'),
    path('directors/', DirectorsAPIView.as_view(), name='directors'),
    path('directors/current/', CurrentDirectorAPIView.as_view(), name='current-director'),
    path('facilities/', FacilitiesAPIView.as_view(), name='facilities'),
    path('statistics/', StatisticsAPIView.as_view(), name='statistics'),
    path('contact/', ContactInfoAPIView.as_view(), name='contact-info'),
]