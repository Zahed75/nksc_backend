from django.urls import path

from journal.views import *

urlpatterns = [
    path("get-all-journals/", JournalListAPIView.as_view()),
    path("create/", JournalCreateAPIView.as_view()),
    path("update/<int:journal_id>/", JournalUpdateAPIView.as_view()),
    path("delete/<int:journal_id>/", JournalDeleteAPIView.as_view()),

    path("filter/",filter_journals),
]
