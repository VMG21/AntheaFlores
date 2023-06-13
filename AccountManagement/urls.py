from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="AccountManagement"

urlpatterns = [
    # Perfil
    path('' , views.userProfile, name="userProfile"),
    path('MiCuenta' , views.myAccount, name="myAccount"),
    
    # Compras
    path('MisPedidos' , views.orderList, name="orderList"),
    # Direcciones
    path('Direcciones' , views.addressList, name="addressList"),
    path('CrearDirección' , views.addressCreate, name="addressCreate"),
    path('ModificarDirección/<int:id>' , views.addressModify, name="addressModify"),
    path('EliminarDirección/<int:id>' , views.addressDelete, name="addressDelete"),
    path('add_product_to_cart/<int:product_id>' , views.add_product_to_cart, name="add_product_to_cart"),
]
