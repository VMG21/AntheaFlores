from django.urls import path
from django.urls.conf import include
from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls'), name="login"),
    path('CrearCuenta',  CreateAccount, name="CreateAccount"),
]
