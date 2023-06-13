from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

app_name="Catalog"

urlpatterns = [
    path('', views.index, name="index"),
    path('Ajax/Search', views.getCards, name="getCards"),
    path('add_product_to_cart/<int:product_id>' , views.add_product_to_cart, name='add_product_to_cart')
]
