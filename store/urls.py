from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'),
    path('create/book/', views.create_book, name='create_book'),
    path('create/item/', views.create_item, name='create_item'),
    # path('create/store/', views.create_store, name='create_store'),
  # path('edit_category/<int:cat_id>/', views.edit_category, name='edit_category'),
]