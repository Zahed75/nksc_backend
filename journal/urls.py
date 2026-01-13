from django.urls import path
from .views import (
    create_journal,
    update_journal,
    get_all_journals,
    delete_journal,
)

urlpatterns = [
    path("journals/", get_all_journals),
    path("journals/create/", create_journal),
    path("journals/<int:journal_id>/update/", update_journal),
    path("journals/<int:journal_id>/delete/", delete_journal),
]
