from django.contrib import admin
from .models import  Book, Item, Order, Store, OrderGroup, Product,ProductGiven,ProductGivenDetail
# Register your models here.


admin.site.register(Book)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderGroup)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(ProductGiven)
admin.site.register(ProductGivenDetail)
