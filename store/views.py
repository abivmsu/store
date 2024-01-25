from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse
from .forms import StoreForm, CategoryForm, BookForm, ItemForm, StoreForm, OrderForm
from django.contrib import messages
from .models import *
from cart.cart import Cart
from django.db import transaction
import datetime
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
    form = BookForm()
    context = {'books':book,'page':page, 'book_form': form}
    return render(request, 'store/store.html', context)

def item_store(request):
    page = 'item'
    item = Store.objects.filter(is_item = True)
    form = ItemForm()
    context = {'items':item ,'page':page,'item_form':form}
    return render(request, 'store/store.html', context)


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            p = 'book'
            existing_book = Book.objects.filter(
                book_name=form.cleaned_data['book_name'],
                grade=form.cleaned_data['grade'],
                pages=form.cleaned_data['pages'],
                subject=form.cleaned_data['subject'],
            ).first()

            if existing_book:
                # If the book exists, redirect to product_detail
                return redirect(reverse('product_detail', kwargs={'product_id': existing_book.id}) + f'?p=book')
            else:
                # If the book doesn't exist, save the form and redirect
                book = form.save()
                return redirect(reverse('product_detail', kwargs={'product_id': book.id}) + f'?p=book')

def add_item(request):
   if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            p = 'item'
            existing_item = Item.objects.filter(
                item_name=form.cleaned_data['item_name'],
               
            ).first()

            if existing_item:
                # If the book exists, redirect to product_detail
                return redirect(reverse('product_detail', kwargs={'product_id': existing_item.id}) + f'?p=item')
            else:
                # If the book doesn't exist, save the form and redirect
                item = form.save()
                return redirect(reverse('product_detail', kwargs={'product_id': item.id}) + f'?p=item')

# detail to add quantity and other like price , unit ... to the cart
def product_detail(request,product_id):
    product_type = request.GET['p']
    if product_type == 'book':
        page = 'book'
        product = Book.objects.get(id = product_id)
        form = OrderForm()
    elif product_type == 'item':
        page = 'item'
        product = Item.objects.get(id = product_id)
        form = OrderForm( )
    context = {'product':product,'page':page, 'form':form}
    return render(request, 'store/product_detail.html', context)

def store_detail(request,store_id):
    product_type = request.GET['p']
    product = Store.objects.get(id = store_id)
    book_form = BookForm(instance= product.books)
    store_form = StoreForm(instance= product)
    item_form = ItemForm(instance= product.items)
    if product_type == 'book':
        if product.books:
            item_form = ItemForm(instance= product.items)
            if request.method == 'POST':
                store_form = StoreForm(request.POST,instance= product)
                book_form = BookForm(request.POST,instance= product.books)
                if store_form.is_valid() and book_form.is_valid():
                    store_form.save()
                    book_form.save()
                #return redirect(reverse('product_detail', kwargs={'product_id': book}) + f'?p=book')
                return redirect('book_store')
    elif product_type == 'item':
        if product.items:
            if request.method == 'POST':
                store_form = StoreForm(request.POST,instance= product)
                item_form = ItemForm(request.POST,instance= product.items)
                if store_form.is_valid() and item_form.is_valid():
                    store_form.save()
                    item_form.save()
                #return redirect(reverse('product_detail', kwargs={'product_id': book}) + f'?p=book')
                return redirect('item_store')
    context = {'product':product, 'book_form':book_form, 'item_form':item_form, 'store_form':store_form}
    return render(request, 'store/store_detail.html', context)


def finish_order(request):
    if request.user.groups.filter(name='Custodian').exists():
        if request.method == 'POST':
            order_for = request.POST.get('order_for')
            order_by = request.POST.get('order_by')
            recieved_by = request.POST.get('recieved_by')
            #if request.user.groups.filter(name='Custodian').exists():
            user = request.user
            order_group = OrderGroup(user=user, 
            order_type='incoming',
            status='Complete',
            order_for= order_for,
            order_by= order_by,
            date=datetime.datetime.today(),
            recieved_by= recieved_by
            )
            order_group.save()
            # Get the cart and iterate through the products
            cart = Cart(request)
            # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Iterate through the cart
            for product_key, product_data in cart.cart.items():
                product_id, product_type = product_key.split('_')

                # Create an instance of the Order model for each product
                order = Order(
                    user=user,
                    quantity=product_data['quantity'],
                    price=product_data['price'],
                    total_price=product_data['quantity'] * product_data['price'],
                    order_type='incoming',  # Set order type as needed
                    unit=product_data['unit'],  # Assuming you want the last unit in the cart
                )
                # Assuming 'books' and 'items' are related names in the Order model
                if product_type == 'book':
                    book = Book.objects.get(id= product_id)
                    order.books=book
                    order.is_book = True
                    store_product, created = Store.objects.get_or_create(
                        books_id=product_id,
                        defaults={'is_book': True}
                    )
                elif product_type == 'item':
                    item = Item.objects.get(id= product_id)
                    order.items = item
                    order.is_item = True
                    store_product, created = Store.objects.get_or_create(
                        items_id=product_id,
                        defaults={'is_item': True}
                    )
                order.save()
                if store_product:
                    store_product.quantity += product_data['quantity']
                    store_product.save()
                order_group.orders.add(order)
        # Clear the cart after completing the orders
        cart.clear()
        order_group = OrderGroup.objects.filter(user = user, order_type= 'incoming')

        return redirect(reverse('orders') + f'?p=gebi')
   
    elif request.user.groups.filter(name='Director').exists():
        if request.method == 'POST':
            order_by = request.POST.get('order_by')
            password = request.POST.get('password')
              # Check if the provided password matches the user's password
            if not request.user.check_password(password):
                messages.error(request, 'Incorrect password. Please try again.')
                return redirect(reverse('list_summary'))
            #if request.user.groups.filter(name='Custodian').exists():
            userr = request.user
            order_group = OrderGroup(user=userr, 
            order_type='outgoing',
            status='Pending',
            order_by= order_by,
            date=datetime.datetime.today(),
            )
            order_group.save()
            # Get the cart and iterate through the products
            cart = Cart(request)
            # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Iterate through the cart
            for product_key, product_data in cart.cart.items():
                product_id, product_type = product_key.split('_')

                # Create an instance of the Order model for each product
                order = Order(
                    user=userr,
                    quantity=product_data['quantity'],
                    # price=product_data['price'],
                    # total_price=product_data['quantity'] * product_data['price'],
                    order_type='outgoing',  # Set order type as needed
                    unit=product_data['unit'],  # Assuming you want the last unit in the cart
                )
                #Assuming 'books' and 'items' are related names in the Order model
                if product_type == 'book':
                    book = Book.objects.get(id= product_id)
                    order.books=book
                    order.is_book = True
                    # store_product, created = Store.objects.get_or_create(
                    #     books_id=product_id,
                    #     defaults={'is_book': True}
                    # )
                elif product_type == 'item':
                    item = Item.objects.get(id= product_id)
                    order.items = item
                    order.is_item = True
                    # store_product, created = Store.objects.get_or_create(
                    #     items_id=product_id,
                    #     defaults={'is_item': True}
                    # )
                order.save()
                # if store_product:
                #     store_product.quantity += product_data['quantity']
                #     store_product.save()
                order_group.orders.add(order)
            # Clear the cart after completing the orders
            cart.clear()
            order_group = OrderGroup.objects.filter(user = userr, order_type= 'outgoing')

            return redirect(reverse('orders') + f'?p=wechi')
        return HttpResponseForbidden('Forbidden')

def orders(request):
    if request.GET['p'] == 'gebi':
        page =  request.GET['p']
        order_group = OrderGroup.objects.filter( user = request.user, order_type= 'incoming')
       

    elif request.GET['p'] =='wechi':
        page =  request.GET['p']
        if request.user.groups.filter(name='Director').exists():
            order_group = OrderGroup.objects.filter( user = request.user, order_type= 'outgoing')
        else:
            order_group = OrderGroup.objects.filter(order_type= 'outgoing')
    context= {'order_group': order_group, 'page':page}
    return render(request, 'order/order.html', context)

def order_detail(request,order_id):
    order = OrderGroup.objects.get(id = order_id)
    context = {'order':order}
    return render(request, 'order/order_detail.html', context)