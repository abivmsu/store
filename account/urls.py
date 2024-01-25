from django.urls import path
from . import views

urlpatterns = [
   path('', views.log_in, name='log_in'),
   path('log_out', views.log_out, name='log_out'),
   path('editProfile', views.editProfile, name='profile'),
   path('create_user', views.create_user, name='create_user'),
   path('create_group', views.create_group, name='create_group'),
   path('user_list', views.user_list, name='user_list'),
   path('deactivate_user', views.deactivate_user, name='deactivate_user'),
  # path('remove-user/<int:user_id>/', views.remove_user, name='remove_user'),
  path('remove_user', views.remove_user, name='remove_user'),
  path('activate_user', views.activate_user, name='activate_user'),
   # path('user/<str:userr_id>/', views.user_detail, name='user_detail'),

  # path('edit_category/<int:cat_id>/', views.edit_category, name='edit_category'),
]