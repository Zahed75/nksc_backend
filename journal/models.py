from django.db import models


class Journal(models.Model):
    title = models.CharField(max_length=255)
    volume = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    issue = models.CharField(max_length=100)
    editor = models.CharField(max_length=255)
    issn = models.CharField(max_length=50, blank=True)
    doi_url = models.URLField(blank=True)

    description = models.TextField()
    pages = models.PositiveIntegerField()
    file_size_mb = models.DecimalField(max_digits=5, decimal_places=2)

    pdf_file = models.FileField(upload_to="journals/")
    preview_image = models.ImageField(upload_to="journal_previews/", blank=True, null=True)

    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title