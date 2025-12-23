from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField("Название", max_length=200)
    author = models.CharField("Автор", max_length=200, blank=True)
    description = models.TextField("Описание", blank=True)
    grade = models.CharField("Класс/уровень", max_length=50, blank=True)
    subject = models.CharField("Предмет", max_length=100, blank=True)
    pdf = models.FileField("PDF файл", upload_to="books/")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="uploaded_books")
    uploaded_at = models.DateTimeField("Загружено", auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title
