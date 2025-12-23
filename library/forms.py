from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "description", "grade", "subject", "pdf"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: Алгебра 7 класс"}),
            "author": forms.TextInput(attrs={"class": "form-control", "placeholder": "Автор (если есть)"}),
            "grade": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: 7 класс"}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: Математика"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Короткое описание"}),
        }

    def clean_pdf(self):
        f = self.cleaned_data.get("pdf")
        if not f:
            raise forms.ValidationError("Нужен PDF файл.")
        name = f.name.lower()
        if not name.endswith(".pdf"):
            raise forms.ValidationError("Можно загружать только файлы PDF.")
        if f.size > 50 * 1024 * 1024:
            raise forms.ValidationError("Файл слишком большой. Максимум 50MB.")
        return f
