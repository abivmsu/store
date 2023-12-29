from django.shortcuts import render, redirect
from .forms import StoreForm, CategoryForm, BookForm, ItemForm, StoreForm
from django.contrib import messages
from .models import *
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
            return redirect('index')  
    else:
        form = BookForm()

    return render(request, 'create_book.html', {'form': form})

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            return redirect('index')  
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
        books = Book.objects.all()
        items = Item.objects.all()
    context = {'form': form, 'books': books, 'items': items}
    return render(request, 'index.html', context )

def book_store(request):
    page = 'book'
    book = Store.objects.filter(is_book = True)
    context = {'books':book,'page':page}
    return render(request, 'store/store.html', context)

def item_store(request):
    page = 'item'
    item = Store.objects.filter(is_item = True)
    print(item)
    context = {'items':item ,'page':page}
    return render(request, 'store/store.html', context)


def add_book(request):
    page = 'book'
    book = Book.objects.all()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('add_book')  
    else:
        form = BookForm()
    context = {'books':book, 'book_form':form ,'page':page}
    return render(request, 'store/add.html', context)

def add_item(request):
    page = 'item'
    item = Item.objects.all()
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            return redirect('add_item')  
    else:
        form = ItemForm()
    context = {'items':item,'item_form':form,'page':page}
    return render(request, 'store/add.html', context)


