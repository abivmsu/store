from django.shortcuts import render, redirect
from .forms import StoreForm, CategoryForm, BookForm, ItemForm, StoreForm
# Create your views here.


# def index(request):
#     if request.method == 'POST':
#         form = StoreForm(request.POST)
#         if form.is_valid():
#             store_instance = form.save()
#             # Optionally, you can perform additional actions here.
#             return redirect('index')  # Replace 'success_page' with your success page URL.
#     else:
#         form = StoreForm()

#     return render(request, 'index.html', {'form': form})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Replace 'success_page' with your success page URL.
    else:
        form = CategoryForm()

    return render(request, 'create_category.html', {'form': form})

def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('index')  # Replace 'create_store' with your desired URL
    else:
        form = BookForm()

    return render(request, 'create_book.html', {'form': form})

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            return redirect('index')  # Replace 'create_store' with your desired URL
    else:
        form = ItemForm()

    return render(request, 'create_item.html', {'form': form})


def index(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Replace 'success_page' with your success page URL.
    else:
        form = StoreForm()

    return render(request, 'index.html', {'form': form})
