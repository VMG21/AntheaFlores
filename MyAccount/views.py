from django.shortcuts import render
from db import models

def product_list(request):
    context = {
        'products': models.Product.all()
    }

    return render(request, "products_list.html", context)
