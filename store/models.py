from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType

from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.

#category of items
class Category (models.Model):
  name = models.CharField( max_length=50)

  def __str__(self):
        return self.name
    

class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default="", blank=True,null=True)
    image = models.ImageField(upload_to = 'uploads/book/') 
    book_name = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)
    pages = models.IntegerField()
    subject = models.CharField(max_length=255)
   
    def __str__(self):
        return self.book_name
        
class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default="", blank=True,null=True)
    image = models.ImageField(upload_to = 'uploads/item/') 
    item_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.item_name

class Order(models.Model):
    ORDER_TYPES = (
          ('incoming', 'Incoming'),
          ('outgoing', 'Outgoing'),
    )    
    UNITS = (
          ('none', 'None'),
          ('liter', 'Liter'),
          ('kg', 'Kilogram'),
          ('packets', 'Packets'),
          ('piece', 'Piece'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    confirmed_quantity = models.IntegerField(default=0)
    issued_quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPES)
    unit = models.CharField(max_length=20, choices=UNITS)
    subunit = models.CharField(max_length=20, choices=UNITS, default='none', blank=True, null=True)
    subunit_quantity = models.IntegerField(blank=True, null=True)
    is_book = models.BooleanField(default=False)
    is_item = models.BooleanField(default=False)
    issued_date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return f"Order from {self.books}, {self.items}"


class OrderGroup(models.Model):
    ORDER_TYPES = (
          ('incoming', 'Incoming'),
          ('outgoing', 'Outgoing'),
    )  
    STATUS = (
          ('Pending', 'Pending'),
          ('Accepted', 'Accepted'),
          ('Complete', 'Complete'),
    )  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPES)
    order_for = models.CharField(max_length=50, blank= True)
    order_by = models.CharField(max_length=50, blank= True)
    recieved_by = models.CharField(max_length=50, blank= True)
    approved_by = models.CharField(max_length=50, blank= True)
    status = models.CharField(max_length=10, choices=STATUS)
    date = models.DateField(default = datetime.datetime.today)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
   
    def __str__(self):
        return f"Order From {self.user}"

class Store(models.Model):
    books = models.ForeignKey(Book,on_delete=models.CASCADE, blank=True, null=True)
    items = models.ForeignKey(Item, on_delete=models.CASCADE,blank=True, null= True)
    quantity = models.IntegerField(default = 0)
    is_book = models.BooleanField(default=False)
    is_item = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.books } - {self.items}"







###############################################################################################################
###############################################################################################################
###############################################################################################################



class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductGiven(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductGivenDetail')
    date_requested = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Product Given"
        verbose_name_plural = "Products Given"

    def __str__(self):
        return f"{self.teacher.username} - {self.date_requested}"

class ProductGivenDetail(models.Model):
    product_given = models.ForeignKey(ProductGiven, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_given = models.DateField()
    date_returned = models.DateField(blank=True, null=True)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Product Given Detail"
        verbose_name_plural = "Product Given Details"

    def __str__(self):
        return f"{self.product.name} - {self.product_given.teacher.username} - {self.date_given}"