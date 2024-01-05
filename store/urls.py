from django.urls import path
from . import views

urlpatterns = [
   path('index', views.index, name='index'),
    path('create/book/', views.create_book, name='create_book'),
    path('create/item/', views.create_item, name='create_item'),

  # Store
    path('book/', views.book_store, name='book_store'),
    path('item/', views.item_store, name='item_store'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('store_detail/<int:store_id>/', views.store_detail, name='store_detail'),

  #order
    path('finish_order', views.finish_order, name='finish_order'),
    # path('item/gebi_book', views.gebi_book_detail, name='gebi_book_detail'),
    # path('item/gebi_item', views.gebi_book_detail, name='gebi_book_detail'),

  #new Book and item
    path('addb/', views.add_book, name='add_book'),
    path('addi/', views.add_item, name='add_item'),
    # path('create/store/', views.create_store, name='create_store'),
]