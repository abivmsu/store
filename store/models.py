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

class Order (models.Model):
    ORDER_TYPES = (
          ('incoming', 'Incoming'),
          ('outgoing', 'Outgoing'),
    )    
    STATUS = (
          ('Pending', 'Pending'),
          ('Accepted', 'Accepted'),
          ('Complete', 'Complete'),
    )
    UNITS = (
          ('litter', 'Litter'),
          ('kg', 'Kilogram'),
          ('packets', 'Packets'),
          ('Piece', 'Piece'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, blank=True)
    items = models.ManyToManyField(Item, blank=True)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =  models.IntegerField(default = 0)
    price = models.DecimalField(max_digits=10, decimal_places=2,default = 0.00)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPES)
    date = models.DateField(default = datetime.datetime.today)
    status = models.CharField(max_length=10, choices=STATUS)
    unit = models.CharField(max_length=20, choices=UNITS)
    order_for = models.CharField(max_length=50, blank= True)
    order_by = models.CharField(max_length=50, blank= True)
    recieved_by = models.CharField(max_length=50, blank= True)
    def __str__(self):
        return f"Order {self.id}"

    def get_books_str(self):
        return ', '.join(str(book) for book in self.books.all())

    def get_items_str(self):
        return ', '.join(str(item) for item in self.items.all())

    def get_full_description(self):
        return f"Books: [{self.get_books_str()}], Items: [{self.get_items_str()}]"

class OrderGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return f"OrderGroup {self.user}"

class Store(models.Model):

    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # product = GenericForeignKey('content_type', 'object_id')
    books = models.ForeignKey(Book,on_delete=models.CASCADE, blank=True, null=True)
    items = models.ForeignKey(Item, on_delete=models.CASCADE,blank=True, null= True)
    quantity = models.IntegerField(default = 0)
    is_book = models.BooleanField(default=False)
    is_item = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.books } - {self.items}"
