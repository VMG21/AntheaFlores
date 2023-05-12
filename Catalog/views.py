from django.shortcuts import render

from db.models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'Catalog/index.html',{
        "products": products
    })