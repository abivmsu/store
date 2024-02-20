from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from store.models import *
from django.http import JsonResponse
# Create your views here.

def list_summary(request):
    cart = Cart(request)
    products = cart.get_prods()
    total_books = cart.total('book')
    total_items = cart.total('item')
    overall_total = cart.calculate_totals()
    total_quantity = cart.total_quantity()
     
    context = {'products': products,
     'total_books': total_books, 
     'total_items': total_items, 
     'overall_total':overall_total,
     'total_quantity':total_quantity
     }
    return render(request, 'list_summary.html', context)


def list_add(request):
  cart = Cart(request)
  
  if request.user.groups.filter(name='Custodian').exists():
   
    if request.POST.get('action') == 'post':
      product_id = int(request.POST.get('product_id'))
      if request.POST.get('product_type') == 'book':
        book = get_object_or_404(Book, id = product_id)
        product_quantity = int(request.POST.get('product_quantity'))
        product_unit = (request.POST.get('product_unit'))
        product_price = float(request.POST.get('product_price'))
        product_type = request.POST.get('product_type')

        product_subunit = (request.POST.get('product_subunit'))
        product_tax = int(request.POST.get('product_tax'))
        product_subunit_quantity = int(request.POST.get('product_subunit_quantity'))
        cart.add(
          product=book,
          quantity = product_quantity, 
          unit = product_unit, 
          price= product_price , 
          product_type = product_type,

          sub_unit = product_subunit, 
          tax = product_tax, 
          subunit_quantity = product_subunit_quantity, 
          )
        
        list_quantity = cart.__len__()
        #response = JsonResponse({'Product Name: ': book.book_name})
        response = JsonResponse({'qty': list_quantity})

      elif request.POST.get('product_type') == 'item': 
        item = get_object_or_404(Item, id = product_id)
        product_quantity = int(request.POST.get('product_quantity'))
        product_unit = (request.POST.get('product_unit'))
        product_price = float(request.POST.get('product_price'))
        product_type = request.POST.get('product_type')
        product_subunit = (request.POST.get('product_subunit'))
        product_tax = int(request.POST.get('product_tax'))
        product_subunit_quantity = int(request.POST.get('product_subunit_quantity'))
       
        cart.add(
          product=item, 
          quantity = product_quantity, 
          unit = product_unit, 
          price= product_price , 
          product_type = product_type,
        
          sub_unit = product_subunit, 
          tax = product_tax, 
          subunit_quantity = product_subunit_quantity
          )
        
        list_quantity = cart.__len__()
        #response = JsonResponse({'Product Name: ': book.book_name})
        response = JsonResponse({'qty': list_quantity})
      # Get Cart Quantity
      #cart_quantity = cart.__len__()
      #response = JsonResponse({'qty': cart_quantity})
      return response
  
  else:
    
    if request.POST.get('action') == 'post':
      product_id = int(request.POST.get('product_id'))
      if request.POST.get('product_type') == 'book':
        book = get_object_or_404(Book, id = product_id)

        product_quantity = int(request.POST.get('product_quantity'))
        product_unit = (request.POST.get('product_unit'))
        product_type = request.POST.get('product_type')

        product_subunit = (request.POST.get('product_subunit'))
        product_subunit_quantity = int(request.POST.get('product_subunit_quantity'))
        cart.add(
          product=book,
          quantity = product_quantity, 
          unit = product_unit, 
          product_type = product_type,
          price= 0 ,
          sub_unit = product_subunit, 
          tax = 0,
          subunit_quantity = product_subunit_quantity, 
          )
        
        list_quantity = cart.__len__()
        #response = JsonResponse({'Product Name: ': book.book_name})
        response = JsonResponse({'qty': list_quantity})

      elif request.POST.get('product_type') == 'item': 
        item = get_object_or_404(Item, id = product_id)
        product_quantity = int(request.POST.get('product_quantity'))
        product_unit = (request.POST.get('product_unit'))
        product_type = request.POST.get('product_type')
        product_subunit = (request.POST.get('product_subunit'))
        product_subunit_quantity = int(request.POST.get('product_subunit_quantity'))
       
        cart.add(
          product=item, 
          quantity = product_quantity, 
          unit = product_unit, 
          price= 0 , 
          product_type = product_type,
        
          sub_unit = product_subunit, 
          tax = 0, 
          subunit_quantity = product_subunit_quantity
          )
        
        list_quantity = cart.__len__()
        #response = JsonResponse({'Product Name: ': book.book_name})
        response = JsonResponse({'qty': list_quantity})
      # Get Cart Quantity
      #cart_quantity = cart.__len__()
      #response = JsonResponse({'qty': cart_quantity})
      return response

def list_update(request):
    cart = Cart(request)
     
    if request.user.groups.filter(name='Custodian').exists():
      if request.POST.get('action') == 'post':
        # Get stuff
        cart_key = request.POST.get('product_id')
        product_quantity = int(request.POST.get('product_quantity'))
        product_price = float(request.POST.get('product_price'))
        # print(cart_key , product_quantity, product_price)
        cart.update(product=cart_key, quantity=product_quantity, price=product_price)

        response = JsonResponse({'qty':product_quantity})
        #return redirect('cart_summary')
        return response
    else:
       if request.POST.get('action') == 'post':
        # Get stuff
        cart_key = request.POST.get('product_id')
        product_quantity = int(request.POST.get('product_quantity'))
        product_price = 0
        # print(cart_key , product_quantity, product_price)
        cart.update(product=cart_key, quantity=product_quantity, price=product_price)

        response = JsonResponse({'qty':product_quantity})
        #return redirect('cart_summary')
        return response

def list_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
      # Get stuff
      cart_key = request.POST.get('product_id')
      print(cart_key)
      cart.remove(product=cart_key)
      response = JsonResponse({'product':cart_key})
      #return redirect('cart_summary')
      return response