from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "grade", "subject", "uploaded_by", "uploaded_at")
    search_fields = ("title", "author", "description", "grade", "subject")
    list_filter = ("grade", "subject", "uploaded_at")
