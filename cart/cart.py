from store.models import *
class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key!  Create one!
        if 'session_key' not in request.session:
          cart = self.session['session_key'] = {}
        # Make sure cart is available on all pages of site
        self.cart = cart
    def add (self, product, quantity, unit, price, product_type, sub_unit,tax,subunit_quantity):
        product_id = str(product.id)
        product_quantity = str(quantity)
        product_unit = str(unit)
        product_price = str(price)

        product_subunit = str(sub_unit)
        product_tax = str(tax)
        product_subunit_quantity = str(subunit_quantity)
      

        # Create a unique key combining product_id and product_type
        cart_key = f"{product_id}_{product_type}"

        # Check if the cart_key is already in the cart
        if cart_key in self.cart:
            # If the entry already exists, update the quantity
            # self.cart[cart_key]['quantity'] += int(product_quantity)
            pass
        else:
            # If the entry does not exist, add a new entry
            self.cart[cart_key] = {
                'quantity': int(product_quantity),
                'unit': product_unit,
                'price': float(product_price),
                'p_type': product_type,
                'sub_unit': product_subunit,
                'subunit_quantity': int(product_subunit_quantity),
                'tax': product_tax,
            }


        self.session.modified = True
    def __len__(self):
		    return len(self.cart)

    def get_prods(self):
        # Get ids from cart
        cart_keys  = self.cart.keys()
        q = self.cart.keys()
        # Use ids to lookup products in database model
        products = []
        for cart_key in cart_keys:
            product_id, product_type = cart_key.split('_')
            if product_type == 'book':
                product = Book.objects.get(id=product_id)
                #product.p_type = product_type
            elif product_type == 'item':
                product = Item.objects.get(id=product_id)
                
            else:
                # Handle other product types or raise an error
                continue

            # Add quantity, unit, and price information to each product
            product.quantity = self.cart[cart_key]['quantity']
            product.unit = self.cart[cart_key]['unit']
            product.price = self.cart[cart_key]['price']
            product.sub_unit = self.cart[cart_key]['sub_unit']
            product.subunit_quantity = self.cart[cart_key]['subunit_quantity']
            product.tax = self.cart[cart_key]['tax']
            product.p_type = product_type

              # Get the store quantity for the product
            if product_type == 'book':
                store_product = Store.objects.get(books=product)
            elif product_type == 'item':
                store_product = Store.objects.get(items=product)
            store_quantity = store_product.quantity

            # Add store quantity to the product
            product.store_quantity = store_quantity
            
            product.total = product.quantity * product.price 
            product.price_tax = product.total * (float(product.tax)/100)
            product.total_price = product.total + product.price_tax 

            products.append(product)

        return products

    def total (self, product_type):
        total = 0
        for cart_key, cart_item in self.cart.items():
            if cart_key.endswith(f"_{product_type}"):
                total += cart_item['quantity'] * cart_item['price']
        return total

    def calculate_totals(self):
        for product_key, product_data in self.cart.items():
            product_id, product_type = product_key.split('_')

            if product_type == 'book':
                product = Book.objects.get(id=product_id)
            elif product_type == 'item':
                product = Item.objects.get(id=product_id)
            else:
                # Handle other product types or raise an error
                continue

            # Calculate total price for each product
            product.total_price = product_data['quantity'] * product_data['price']
            total = product_data['quantity'] * product_data['price'] 
            tax_price = total * (float( product_data['tax'])/100)
            total_price = total + tax_price
        # Calculate overall total
        #overall_total = sum(product_data['quantity'] * product_data['price'] for product_data in self.cart.values())
        overall_total = sum(total_price for product_data in self.cart.values())

        return overall_total
    
    def total_quantity(self):
        total_quanitity = 0
        for product_key, product_data in self.cart.items():
            product_id, product_type = product_key.split('_')

            if product_type == 'book':
                product = Book.objects.get(id=product_id)
            elif product_type == 'item':
                product = Item.objects.get(id=product_id)
            else:
                # Handle other product types or raise an error
                continue

            # Calculate total price for each product
            product.quantity = product_data['quantity']
            total_quanitity += product.quantity 
        return total_quanitity

    def update(self, product, quantity,price):
        product_id, product_type = product.split('_')
        product_quantity = int(quantity)
        product_price = float(price)

        # If the product is already in the cart, update the quantity and price
        if product in self.cart:
            self.cart[product]['quantity'] = product_quantity
            self.cart[product]['price'] = product_price
            if  self.cart[product]['sub_unit'] == 'none':
                self.cart[product]['subunit_quantity'] = product_quantity
            else:
                pass
        self.session.modified = True
        
        #return {'success': True}
        return self.cart

    def remove(self, product):
        # If the product is already in the cart, update the quantity and price        
        if product in self.cart:
            del self.cart[product]
            self.session.modified = True
    
    def clear(self):
        self.cart = {}
        self.session['session_key'] = {}
        self.session.modified = True