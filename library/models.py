from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from cloudinary.utils import cloudinary_url


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # PDF хранится как RAW в Cloudinary
    pdf = models.FileField(
        upload_to="books/",
        storage=RawMediaCloudinaryStorage(),
        blank=True,
        null=True
    )

    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def pdf_view_url(self):
        """
        URL для просмотра (вкладка/iframe).
        """
        if not self.pdf:
            return ""
        # storage уже отдаёт secure URL, но на всякий случай:
        return self.pdf.url

    @property
    def pdf_download_url(self):
        """
        URL для скачивания (Cloudinary flag attachment).
        Работает надёжнее, чем HTML download.
        """
        if not self.pdf:
            return ""

        # В Cloudinary public_id обычно хранится вместе с папкой (books/xxx)
        public_id = self.pdf.name  # например: books/filename.pdf

        url, _ = cloudinary_url(
            public_id,
            resource_type="raw",
            flags="attachment",
            secure=True
        )
        return url
