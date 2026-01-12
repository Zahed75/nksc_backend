from django.urls import path
from journal.views import *

urlpatterns = [
    path('journals/', journal_list, name='journal-list'),
    path('journals/create/', journal_create, name='journal-create'),
]
