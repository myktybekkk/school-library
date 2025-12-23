from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm


@login_required
def book_list(request):
    books = Book.objects.order_by("-uploaded_at")
    return render(request, "library/book_list.html", {"books": books})


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # если у тебя есть логика teacher/админ — оставь свою
    is_teacher = request.user.is_staff or request.user.is_superuser
    return render(request, "library/book_detail.html", {"book": book, "is_teacher": is_teacher})


@login_required
def book_add(request):
    is_teacher = request.user.is_staff or request.user.is_superuser
    if not is_teacher:
        return redirect("book_list")

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by = request.user
            obj.save()
            return redirect("book_list")
    else:
        form = BookForm()

    return render(request, "library/book_form.html", {"form": form})


@login_required
def book_edit(request, pk):
    is_teacher = request.user.is_staff or request.user.is_superuser
    if not is_teacher:
        return redirect("book_list")

    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(request, "library/book_form.html", {"form": form, "book": book})


@login_required
def book_delete(request, pk):
    is_teacher = request.user.is_staff or request.user.is_superuser
    if not is_teacher:
        return redirect("book_list")

    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")

    return render(request, "library/book_confirm_delete.html", {"book": book})
