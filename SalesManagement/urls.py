from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="SalesManagement"

urlpatterns = [
    path('clientBlock/<int:id>', views.clientBlock, name="clientBlock"),
    path('ListaClientes', views.clientList, name="clientList"),
  
]
