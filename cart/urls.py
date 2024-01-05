from django.urls import path
from . import views

urlpatterns = [
  path('', views.list_summary, name="list_summary"),
	path('add/', views.list_add, name="list_add"),
	path('delete/', views.list_delete, name="list_delete"),
	path('update/', views.list_update, name="list_update"),
  # path('edit_category/<int:cat_id>/', views.edit_category, name='edit_category'),
]