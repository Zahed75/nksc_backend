from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.documents.models import Document
from wagtail.images.models import Image
from wagtail.api import APIField


class JournalPage(Page):
    volume = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    issue = models.CharField(max_length=100)
    editor = models.CharField(max_length=255)
    issn = models.CharField(max_length=50, blank=True)
    doi_url = models.URLField(blank=True)

    description = RichTextField()
    pages = models.PositiveIntegerField()
    file_size_mb = models.DecimalField(max_digits=5, decimal_places=2)

    journal_file = models.ForeignKey(
        Document, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    preview_image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("volume"),
                FieldPanel("year"),
                FieldPanel("issue"),
                FieldPanel("editor"),
                FieldPanel("issn"),
                FieldPanel("doi_url"),
            ],
            heading="Journal Metadata",
        ),
        FieldPanel("description"),
        MultiFieldPanel(
            [
                FieldPanel("pages"),
                FieldPanel("file_size_mb"),
                FieldPanel("journal_file"),
                FieldPanel("preview_image"),
            ],
            heading="Files & Media",
        ),
    ]

    api_fields = [
        APIField("title"),
        APIField("volume"),
        APIField("year"),
        APIField("issue"),
        APIField("editor"),
        APIField("issn"),
        APIField("doi_url"),
        APIField("description"),
        APIField("pages"),
        APIField("file_size_mb"),
        APIField("journal_file"),
        APIField("preview_image"),
    ]
