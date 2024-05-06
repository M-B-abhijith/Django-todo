# todo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Add a URL pattern for the empty path
    path('', views.signup_view, name='signup'),
    # Add other URL patterns
    # path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Add other URLs for todo dashboard and tasks

    # path('todo_dashboard/', views.todo_dashboard, name='todo_dashboard'),



        path('todo_dashboard/<int:user_id>/', views.todo_dashboard, name='todo_dashboard'),

    # path('mark_completed/<int:task_id>/', views.mark_completed, name='mark_completed'),
   

       path('mark_completed/<int:task_id>/', views.mark_completed, name='mark_completed'),  # Include task_id
   
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),



]




#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx#