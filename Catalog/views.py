import json
import time
from django.shortcuts import render

from db.models import Product

# Create your views here.
def index(request):
    return render(request, 'Catalog/index.html')


def getCards(request):
    time.sleep(1)
    json_data = json.loads(request.body)
    search = json_data['jsonBody']['search']
    print(search)
    if search == "" or search == None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(name__icontains=search)
    return render(request, 'Catalog/cards.html',{
        "products": products
    })