from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('delete/<int:identifier>/', views.delete_todo, name='delete'),
    path('update/<int:identifier>/', views.update_todo, name='update'),
    path('complete/<int:identifier>/', views.toggle_complete_todo, name='complete'),
]