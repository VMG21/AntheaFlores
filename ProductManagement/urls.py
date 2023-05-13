from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="ProductManagement"

urlpatterns = [

    path('', views.index, name="index"),
    path('EditarProducto/<int:id>', views.productModify, name="productModify"),
    path('productDelete/<int:id>', views.productDelete, name="productDelete"),
    path('CrearProducto', views.productCreate, name="productCreate"),
    path('ListaProductos', views.productList, name="productList")
]
