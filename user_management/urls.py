from django.urls import path
from .views import *

urlpatterns = [
    path('chairman/current/',get_current_chairman)
]