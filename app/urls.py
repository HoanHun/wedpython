from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='dangky'),
    path('login/', views.login_page, name='dangnhap'),
    path('logout/', views.logout_page, name='logout'),
    path('search/', views.search, name='timkiem'),
    path('category/', views.category, name='category'),
    path('detail/', views.detail, name='xemct'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('updateitem/', views.updateItem, name='update_item'),
    
]