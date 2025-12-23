from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "grade", "subject", "description", "pdf"]

    def clean_pdf(self):
        f = self.cleaned_data.get("pdf")
        if not f:
            return f

        name = f.name.lower()
        if not name.endswith(".pdf"):
            raise forms.ValidationError("Можно загрузить только PDF файл.")

        # лимит на размер (например 25MB)
        if f.size > 25 * 1024 * 1024:
            raise forms.ValidationError("PDF слишком большой. Максимум 25MB.")

        return f
