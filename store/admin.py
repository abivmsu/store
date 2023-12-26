from django.contrib import admin
from .models import Category, Book, Item, Order, Store
# Register your models here.

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Store)
