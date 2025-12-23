from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Book
from .forms import BookForm

def is_teacher(user):
    return user.is_authenticated and user.groups.filter(name="Teachers").exists()

@login_required
def book_list(request):
    q = request.GET.get("q", "").strip()
    subject = request.GET.get("subject", "").strip()
    grade = request.GET.get("grade", "").strip()

    books = Book.objects.all()

    if q:
        books = books.filter(
            Q(title__icontains=q) |
            Q(author__icontains=q) |
            Q(description__icontains=q)
        )
    if subject:
        books = books.filter(subject__icontains=subject)
    if grade:
        books = books.filter(grade__icontains=grade)

    subjects = Book.objects.exclude(subject="").values_list("subject", flat=True).distinct()
    grades = Book.objects.exclude(grade="").values_list("grade", flat=True).distinct()

    return render(request, "library/book_list.html", {
        "books": books,
        "q": q,
        "subject": subject,
        "grade": grade,
        "subjects": subjects,
        "grades": grades,
        "is_teacher": is_teacher(request.user),
    })

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "library/book_detail.html", {
        "book": book,
        "is_teacher": is_teacher(request.user),
    })

@user_passes_test(is_teacher)
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.uploaded_by = request.user
            book.save()
            messages.success(request, "Книга добавлена.")
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "library/book_form.html", {"form": form, "mode": "create"})

@user_passes_test(is_teacher)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            updated = form.save(commit=False)
            if updated.uploaded_by is None:
                updated.uploaded_by = request.user
            updated.save()
            messages.success(request, "Книга обновлена.")
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, "library/book_form.html", {"form": form, "mode": "edit", "book": book})

@user_passes_test(is_teacher)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Книга удалена.")
        return redirect("book_list")
    return render(request, "library/book_confirm_delete.html", {"book": book})
