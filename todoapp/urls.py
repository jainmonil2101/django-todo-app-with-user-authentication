from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('create', views.TaskCreate.as_view(), name='create'),
    path('update/<int:pk>', views.TaskUpdate.as_view(), name='update'),
    path('delete/<int:task_pk>', views.deletetask, name='delete'),
    path('complete/<int:task_pk>', views.complete, name='complete'),
    path('incomplete/<int:task_pk>', views.incomplete, name='incomplete'),

]