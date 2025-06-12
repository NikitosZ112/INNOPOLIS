from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),         
    path('register/', views.register, name='register'), 
    path('login/', views.login_view, name='login'),
    path('success-login/', views.success_login, name='success_login'),     
]