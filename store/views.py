from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden,JsonResponse
from django.urls import reverse
from .forms import StoreForm, CategoryForm, BookForm, ItemForm, StoreForm, OrderForm
from django.contrib import messages
from .models import *
from cart.cart import Cart
from django.db import transaction
import datetime , json
from django.views.decorators.http import require_POST
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
   # Calculate the total orders, total items, total books, and other data
    total_orders = Order.objects.count()
    total_items = Item.objects.count()
    total_books = Book.objects.count()

    # You can add more calculations based on your needs

    # Get a list of books, items, and orders to pass to the template
    books = Book.objects.all()
    items = Item.objects.all()
    orders = Order.objects.all()

    # Prepare the context dictionary with the calculated values and data
    context = {
        'total_orders': total_orders,
        'total_items': total_items,
        'total_books': total_books,
        'books': books,
        'items': items,
        'orders': orders,
    }

    # Render the template with the context
    return render(request, 'index.html', context)

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
            overall_total = request.POST.get('overall_total')
            #if request.user.groups.filter(name='Custodian').exists():
            user = request.user
            order_group = OrderGroup(user=user, 
            order_type='incoming',
            status='Complete',
            order_for= order_for,
            order_by= order_by,
            date=datetime.datetime.today(),
            recieved_by= recieved_by,
            total_price= overall_total
            )
            order_group.save()
            # Get the cart and iterate through the products
            cart = Cart(request)
            # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Iterate through the cart
            for product_key, product_data in cart.cart.items():
                product_id, product_type = product_key.split('_')
                
                total = product_data['quantity'] * product_data['price'] 
                tax_price = total * (float( product_data['tax'])/100)
                total_price = total + tax_price
                # Create an instance of the Order model for each product
                order = Order(
                    user=user,
                    quantity=product_data['quantity'],
                    subunit_quantity=product_data['subunit_quantity'],
                    price= total,
                    tax= product_data['tax'],
                    total_price= total_price,
                    order_type='incoming',  # Set order type as needed
                    unit=product_data['unit'],  # Assuming you want the last unit in the cart
                    subunit=product_data['sub_unit'],  # Assuming you want the last unit in the cart
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
                    store_product.quantity += product_data['subunit_quantity']
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
        elif request.user.groups.filter(name='Custodian').exists():
            order_group = OrderGroup.objects.filter(order_type= 'outgoing')
        else:
            order_group = OrderGroup.objects.filter(order_type= 'outgoing')
    context= {'order_group': order_group, 'page':page}
    return render(request, 'order/order.html', context)

def order_detail(request,order_id):
    order = OrderGroup.objects.get(id = order_id)
    context = {'order':order}
    return render(request, 'order/order_detail.html', context)




@require_POST
def confirm_all_quantities(request):
    try:
        ordergroup_id = int(request.POST.get('ordergroup_id'))
        quantities_data = json.loads(request.POST.get('confirmed_quantities'))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid data format'}, status=400)

    try:
        ordergroup = OrderGroup.objects.get(id=ordergroup_id)
    except OrderGroup.DoesNotExist:
        return JsonResponse({'error': f'OrderGroup with ID {ordergroup_id} does not exist'}, status=404)

    for item_data in quantities_data:
        try:
            item_id = int(item_data['productId'])
            quantity = int(item_data['quantity'])
            item = ordergroup.orders.get(id=item_id)
            item.confirmed_quantity = quantity
            item.save()
        except (ValueError, TypeError, Order.DoesNotExist):
            return JsonResponse({'error': 'Invalid product data'}, status=400)
    ordergroup.status='Accepted'
    ordergroup.save()
    return JsonResponse({'success': 'Confirmed quantities updated successfully'})


@require_POST
def issue_quantities(request):
    try:
        ordergroup_id = int(request.POST.get('ordergroup_id'))
        quantities_data = json.loads(request.POST.get('issued_quantities'))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid data format'}, status=400)

    try:
        ordergroup = OrderGroup.objects.get(id=ordergroup_id)
    except OrderGroup.DoesNotExist:
        return JsonResponse({'error': f'OrderGroup with ID {ordergroup_id} does not exist'}, status=404)

    for item_data in quantities_data:
        try:
            item_id = int(item_data['productId'])
            quantity = int(item_data['quantity'])
            product = ordergroup.orders.get(id=item_id)
            if product.is_book  == True:
                store_book = Store.objects.get(books=product.books)
                store_book.quantity -= quantity
                store_book.save()
            elif product.is_item == True:
                store_item =Store.objects.get(items=product.items)
                store_item.quantity -= quantity
                store_item.save()
            product.issued_quantity = quantity
            product.save()
        except (ValueError, TypeError, Order.DoesNotExist):
            return JsonResponse({'error': 'Invalid product data'}, status=400)
    ordergroup.status='Complete'
    ordergroup.save()
    return JsonResponse({'success': 'issued quantities updated successfully'})


@require_POST
def remove_order(request):
    # Get the product ID from the POST data
    product_id = request.POST.get('product_id')
    ordergroup_id = int(request.POST.get('ordergroup_id'))
    try:
        ordergroup = OrderGroup.objects.get(id=ordergroup_id)
    except OrderGroup.DoesNotExist:
        return JsonResponse({'error': f'OrderGroup with ID {ordergroup_id} does not exist'}, status=404)
    # Retrieve the order to be removed
    print(ordergroup.orders.count())
    order_to_remove = get_object_or_404(Order, id=product_id)
    if ordergroup.orders.count() == 1:
        order_to_remove.delete()
        ordergroup.delete()
        return JsonResponse({'success': True, 'redirect': 'store/orders?p=wechi'})
    else:
        order_to_remove.delete()
        # Perform the removal logic, you can customize this based on your needs
    # Return a JSON response indicating success
    return JsonResponse({'message': 'Order removed successfully'})