from django.urls import path
from . import views

urlpatterns = [
   path('index', views.index, name='index'),
   
  # Store
    path('book/', views.book_store, name='book_store'),
    path('item/', views.item_store, name='item_store'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('store_detail/<int:store_id>/', views.store_detail, name='store_detail'),

  #order
    path('finish_order', views.finish_order, name='finish_order'),
    path('orders', views.orders, name='orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('confirm_all_quantities/', views.confirm_all_quantities, name='confirm_all_quantities'),
    path('issue_quantities/', views.issue_quantities, name='issue_quantities'),
    path('remove_order', views.remove_order, name='remove_order'),
    # path('item/gebi_book', views.gebi_book_detail, name='gebi_book_detail'),
    # path('item/gebi_item', views.gebi_book_detail, name='gebi_book_detail'),

  #new Book and item
    path('addb/', views.add_book, name='add_book'),
    path('addi/', views.add_item, name='add_item'),
    # path('create/store/', views.create_store, name='create_store'),


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:pk>/update/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),

# add product name    
    path('add_product', views.add_product, name='add_product'),

    path('teachers_list', views.teachers_list, name='teachers_list'),
    path('asrekeb', views.add_product_given, name='asrekeb'),



    path('items_report/', views.items_report, name='items_report'),
    path('books_report/', views.books_report, name='books_report'),

    path('wechi_report/<int:order_id>/', views.wechi_report, name='wechi_report'),
    path('gebi_report/<int:order_id>/', views.gebi_report, name='gebi_report'),

 path('generate_pdf_report/', views.generate_pdf_report, name='generate_pdf_report'),

]

