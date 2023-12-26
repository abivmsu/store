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
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =  models.IntegerField(default = 1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPES)
    date = models.DateField(default = datetime.datetime.today)
    status = models.CharField(max_length=10, choices=STATUS)
    unit = models.CharField(max_length=20, choices=UNITS)

    def __str__(self):
        return self.user

class Store(models.Model):

    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # product = GenericForeignKey('content_type', 'object_id')
    books = models.ManyToManyField(Book, blank=True)
    items = models.ManyToManyField(Item, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.books.all() } - {self.items.all()}"
