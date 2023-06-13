from datetime import date
import json
import time
from db.models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from db.models import Product

# Create your views here.
def index(request):
    return render(request, 'Catalog/index.html')

@csrf_exempt
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

@login_required
def add_product_to_cart(request, product_id):
    if request.method == "POST":
        quantity = 1
        product = Product.objects.get(id=product_id)
        if Order.objects.filter(client=request.user, status="Carrito").exists():
            order = Order.objects.get(client=request.user, status="Carrito")
        else:
            order = Order.objects.create(client=request.user, status="Carrito", total=0, ordered_date=date.today(), address)
        orderProduct = OrderProduct.objects.create(order=order, product=product, quantity=quantity, price=product.price)
        order.total += orderProduct.price
        order.save()
        return redirect('AccountManagement:orderList')
